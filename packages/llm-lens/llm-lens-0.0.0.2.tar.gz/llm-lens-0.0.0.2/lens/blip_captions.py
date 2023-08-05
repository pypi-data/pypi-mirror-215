from torchvision import transforms
from PIL import Image
import torch
from datasets import load_dataset, load_from_disk, Dataset
from argparse import ArgumentParser, ArgumentTypeError
import torch.distributed as dist
import itertools
import shutil
import os
from tqdm import tqdm
from torch.distributed import init_process_group, destroy_process_group
import datetime
from transformers import AutoProcessor, BlipForConditionalGeneration
import joblib
from lens.utils import create_sampler, ddp_setup, is_main_process, create_dataloader, default_device
from pathlib import Path


def get_caption_model(model_name, load_8bit=False, device=default_device):
    if load_8bit:
        model = BlipForConditionalGeneration.from_pretrained(model_name,
                                                             torch_dtype=torch.float32 if device=="cpu" else torch.float16,
                                                             device_map={
                                                                 '': device},
                                                             load_in_8bit=True)
    else:
        model = BlipForConditionalGeneration.from_pretrained(model_name,
                                                             torch_dtype=torch.float32 if device=="cpu" else torch.float16)
        model = model.eval()
        model = model.to(device)
    return model


def get_column_name(args):
    column_name = f"blip_caption_{str(args.sample)}_beams_{args.num_beams}_{args.model_name.replace('/','_').replace('-','_')}_max_length_{args.max_length}_hf"
    if args.prefix_text != 'a picture of':
        column_name = f"{column_name}_{args.prefix_text}"
    return column_name


class Captioner:
    def __init__(self,
                 model_name="Salesforce/blip-image-captioning-large",
                 load_8bit=False,
                 device=default_device):
        self.model = get_caption_model(
            model_name, load_8bit=load_8bit, device=device)
        self.transform = AutoProcessor.from_pretrained(model_name)
        self.device = device

    def get_captions(self,
                     ds,
                     sample=False,
                     num_beams=5,
                     top_p=1,
                     max_length=30,
                     min_length=10,
                     batch_size=8,
                     num_workers=0,
                     id_col="id",
                     image_col="image",
                     prefix_text="a picture of",
                     distributed=False):

        dataset = ImageDataset(
            ds, self.transform, id_col=id_col, image_col=image_col, prefix_text=prefix_text)
        sampler = create_sampler(dataset, distributed=distributed)
        dataloader = create_dataloader(
            dataset, sampler, batch_size=batch_size, num_workers=num_workers)
        result = []
        for batch in tqdm(dataloader):
            with torch.no_grad():
                pixel_values = batch['pixel_values'].to(
                    self.device, self.model.dtype)
                input_ids = batch['input_ids'].to(self.device)
                image_id = batch['id']
                len_text = batch['len_text_input']
                captions_ids = self.model.generate(pixel_values=pixel_values,
                                                   input_ids=input_ids,
                                                   do_sample=sample,
                                                   num_beams=num_beams,
                                                   top_p=top_p,
                                                   max_length=max_length,
                                                   min_length=min_length)

            captions = self.transform.batch_decode(
                captions_ids, skip_special_tokens=True)

            for caption, img_id, len_ in zip(captions, image_id, len_text):
                result.append({id_col: img_id.item(),
                               "caption": caption[len_:].strip()})
            del pixel_values, captions_ids
        result_ds = Dataset.from_dict(
            {key: [d[key] for d in result] for key in result[0]})
        return result_ds

    def get_intensive_captions(self,
                               ds,
                               batch_size=8,
                               num_workers=0,
                               id_col="id",
                               image_col="image",
                               prefix_text="a picture of",
                               top_k=50,
                               num_captions=100,
                               distributed=False):

        dataset = ImageDataset(
            ds, self.transform, id_col=id_col, image_col=image_col, prefix_text=prefix_text)
        sampler = create_sampler(dataset, distributed=distributed)
        dataloader = create_dataloader(
            dataset, sampler, batch_size=batch_size, num_workers=num_workers)
        result = []

        for batch in tqdm(dataloader):
            with torch.no_grad():
                pixel_values = batch['pixel_values'].to(
                    self.device, self.model.dtype)
                input_ids = batch['input_ids'].to(self.device)
                attention_mask = batch['attention_mask'].to(self.device)
                image_ids = batch['id']
                caption_ids = self.model.generate(pixel_values=pixel_values,
                                                  input_ids=input_ids,
                                                  attention_mask=attention_mask,
                                                  max_length=30,
                                                  min_length=0,
                                                  do_sample=True,
                                                  top_p=1,
                                                  top_k=top_k,
                                                  num_return_sequences=num_captions,
                                                  repetition_penalty=1)

            captions_text = self.transform.batch_decode(
                caption_ids, skip_special_tokens=True)
            captions_text = [caption[12:].strip() for caption in captions_text]
            captions_text = [captions_text[i:i+num_captions]
                             for i in range(0, len(captions_text), num_captions)]

            for caption, img_id in zip(captions_text, image_ids):
                result.append({id_col: img_id.item(), "caption": caption})
            del pixel_values, input_ids, attention_mask, caption_ids

        result_ds = Dataset.from_dict(
            {key: [d[key] for d in result] for key in result[0]})
        return result_ds


class ImageDataset:
    def __init__(self,
                 ds,
                 transform,
                 id_col="id",
                 image_col="image",
                 prefix_text="a picture of",
                 ):

        self.ds = ds
        self.transform = transform
        self.prefix_text = prefix_text
        self.id_col = id_col
        self.image_col = image_col

    def __getitem__(self, idx):
        row = self.ds[idx]
        image, id = row[self.image_col].convert('RGB'), row[self.id_col]
        len_text_input = len(self.prefix_text)
        inputs = self.transform(image,
                                text=self.prefix_text,
                                return_tensors="pt")
        pixel_values = inputs['pixel_values'].squeeze(0)
        input_ids = inputs['input_ids'].squeeze(0)
        attention_mask = inputs['attention_mask'].squeeze(0)
        return {'pixel_values': pixel_values,
                'input_ids': input_ids,
                'len_text_input': len_text_input,
                'attention_mask': attention_mask,
                'id': torch.tensor(id, dtype=torch.int32)}

    def __len__(self):
        return len(self.ds)


def parse_args():
    args = ArgumentParser(description="")
    # Dataset variables
    args.add_argument('--dataset_name',
                      required=True,
                      type=str,
                      default='Multimodal-Fatima/OxfordPets')

    args.add_argument('--dataset_split',
                      required=True,
                      type=str,
                      default='test')
    args.add_argument('--id_col', type=str, default='id')
    args.add_argument('--image_col', type=str, default='image')
    args.add_argument('--save_disk', action="store_true")

    # Model variables
    args.add_argument('--model_name', required=True, type=str,
                      default='Salesforce/blip2-opt-6.7b')
    args.add_argument('--load_8bit', action="store_true")
    args.add_argument('--sample', action="store_true")
    args.add_argument('--prefix_text', type=str, default='a picture of')
    args.add_argument('--num_beams', type=int, default=5)
    args.add_argument('--top_p', type=float, default=1)
    args.add_argument('--max_length', type=int, default=30)
    args.add_argument('--min_length', type=int, default=10)

    # Parameters
    args.add_argument('--batch_size', type=int, default=8)
    args.add_argument('--num_workers', type=int, default=0)

    # Whether to do intensive or regular captioning
    args.add_argument('--intensive', action="store_true")
    args.add_argument('--top_k', type=int, default=50)
    args.add_argument('--num_captions', type=int, default=100)

    args = args.parse_args()
    return args


def main():
    num_tasks = int(os.environ["WORLD_SIZE"])
    global_rank = int(os.environ["RANK"])
    local_rank = int(os.environ["LOCAL_RANK"])
    args = parse_args()
    ds = load_dataset(args.dataset_name, split=args.dataset_split)
    captioner = Captioner(
        args.model_name, load_8bit=args.load_8bit, device=local_rank)
    if args.intensive:
        result_ds = captioner.get_intensive_captions(ds,
                                                     batch_size=args.batch_size,
                                                     num_workers=args.num_workers,
                                                     id_col=args.id_col,
                                                     image_col=args.image_col,
                                                     prefix_text=args.prefix_text,
                                                     top_k=args.top_k,
                                                     num_captions=args.num_captions,
                                                     distributed=True)
    else:
        result_ds = captioner.get_captions(ds,
                                           sample=args.sample,
                                           num_beams=args.num_beams,
                                           top_p=args.top_p,
                                           max_length=args.max_length,
                                           min_length=args.min_length,
                                           batch_size=args.batch_size,
                                           num_workers=args.num_workers,
                                           id_col=args.id_col,
                                           image_col=args.image_col,
                                           prefix_text=args.prefix_text,
                                           distributed=True)

    os.makedirs(Path(__file__).parent /
                "blip_caption_tmp_folder/", exist_ok=True)
    result = []
    for item in result_ds:
        result.append(item)
    joblib.dump(result, Path(__file__).parent /
                f"blip_caption_tmp_folder/data_{global_rank}.json")
    dist.barrier()

    if is_main_process():
        result = []
        dict_captions = {}

        for rank in range(num_tasks):
            result_file = Path(__file__).parent / \
                f"blip_caption_tmp_folder/data_{rank}.json"
            res = joblib.load(result_file)
            result += res

        for res in result:
            dict_captions[res[args.id_col]] = res['caption']

        # Create dataset
        try:
            ds = load_dataset(args.dataset_name,
                              split=args.dataset_split)
        except:
            ds = load_from_disk(args.dataset_name)

        ds = ds.map(lambda example: {get_column_name(
            args): dict_captions[example[args.id_col]]})

        if args.save_disk:
            ds.save_to_disk(f"{args.dataset_name}_captions")
            # remove
            shutil.rmtree(args.dataset_name)
            # rename file
            os.rename(f"{args.dataset_name}_captions", args.dataset_name)
        else:
            ds.push_to_hub(args.dataset_name)


if __name__ == "__main__":
    ddp_setup()
    main()
    destroy_process_group()
