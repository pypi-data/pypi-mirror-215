from datasets import load_dataset, load_from_disk, Dataset
import torch
from argparse import ArgumentParser, ArgumentTypeError
import torch.distributed as dist
from tqdm import tqdm
import joblib
import itertools
import shutil
import os
import subprocess
import open_clip
from transformers import CLIPModel, CLIPProcessor
from torch.distributed import destroy_process_group
import datetime
from pathlib import Path
import huggingface_hub
from lens.utils import ddp_setup, create_sampler, create_dataloader, is_main_process, default_device

DICT_CLIP_NAME = {'openai/clip-vit-large-patch14': 'ViT_L_14',
                  'openai/clip-vit-base-patch16': 'ViT_B_16',
                  'openai/clip-vit-base-patch32': 'ViT_B_32',
                  'hf-hub:laion/CLIP-ViT-H-14-laion2B-s32B-b79K': 'LAION_ViT_H_14_2B',
                  'hf-hub:laion/CLIP-ViT-bigG-14-laion2B-39B-b160k': 'LAION_ViT_bigG_14_2B'}


def flatten(l):
    return [item for sublist in l for item in sublist]


class OpenaiclipDataset:
    def __init__(self, ds, transform, image_col, id_col):
        self.ds = ds
        self.image_col
        self.id_col
        self.transform = transform

    def _load_transform(self):
        return CLIPProcessor.from_pretrained(self.vision_encoder_name)

    def get_model(self):
        return CLIPModel.from_pretrained(self.vision_encoder_name)

    def __getitem__(self, idx):
        row = self.ds[idx]
        image = row[self.image_col].convert('RGB')
        id = row[self.id_col]

        image = self.transform(images=image, return_tensors="pt")[
            'pixel_values'].squeeze(0)
        return {'image': image,
                'id': torch.tensor(id, dtype=torch.int32)}

    def __len__(self):
        return len(self.ds)


class LaionclipDataset:
    def __init__(self, ds, transform, image_col, id_col):
        self.ds = ds
        self.image_col = image_col
        self.id_col = id_col
        self.transform = transform

    def __getitem__(self, idx):
        row = self.ds[idx]
        image = row[self.image_col].convert('RGB')
        id = row[self.id_col]

        image = self.transform(image)
        return {'image': image,
                'id': torch.tensor(id, dtype=torch.int32)}

    def __len__(self):
        return len(self.ds)


class Tagger:
    def __init__(self,
                 vision_encoder_name="hf-hub:laion/CLIP-ViT-H-14-laion2B-s32B-b79K",
                 dataset_vocab="Multimodal-Fatima/descriptors-text-davinci-003",
                 split_vocab="full",
                 zeroshot_weights="zw_attributes_laion_ViT_H_14_2B_descriptors_text_davinci_003_full.pt",
                 device=default_device):

        self.device = device

        if 'openai' in vision_encoder_name:
            self.transform = CLIPProcessor.from_pretrained(vision_encoder_name)
            self.model = CLIPModel.from_pretrained(
                vision_encoder_name).to(self.device)
            self.dataset_class = OpenaiclipDataset

        elif 'laion' in vision_encoder_name:
            model_and_transform = open_clip.create_model_and_transforms(
                vision_encoder_name)
            self.model = model_and_transform[0].to(self.device)
            self.transform = model_and_transform[2]
            self.dataset_class = LaionclipDataset

        self.vocabulary = flatten(load_dataset(
            dataset_vocab, split=split_vocab)['prompt_descriptions'])

        huggingface_hub.hf_hub_download(repo_id="Multimodal-Fatima/AttributesCLIP", filename=zeroshot_weights, local_dir=str(Path(__file__).parent / "weights"))
        self.zeroshot_weights = torch.load(
            str(Path(__file__).parent / f"weights/{zeroshot_weights}"), map_location=self.device).float()

    def get_tags(self,
                 ds,
                 image_col="image",
                 id_col="id",
                 top_k=5,
                 contrastive_th=0.2,
                 batch_size=8,
                 num_workers=0,
                 distributed_sampling=False):

        dataset = self.dataset_class(ds, self.transform, image_col, id_col)

        sampler = create_sampler(dataset, distributed=distributed_sampling)
        dataloader = create_dataloader(
            dataset, sampler, batch_size=batch_size, num_workers=num_workers)

        result = []

        for batch in tqdm(dataloader):
            with torch.no_grad():
                image = batch['image'].to(self.device)
                image_id = batch['id']
                try:
                    image_features = self.model.encode_image(image)
                except:
                    image_features = self.model.get_image_features(
                        pixel_values=image)

                image_features /= image_features.norm(dim=-1, keepdim=True)
                text_scores = image_features @ self.zeroshot_weights
                del image_features
                torch.cuda.empty_cache()
                top_scores, top_indexes = text_scores.float().cpu().topk(k=top_k, dim=-1)
                for scores, indexes, _id in zip(top_scores, top_indexes, image_id):
                    filter_indexes = indexes[scores >= contrastive_th]
                    if len(filter_indexes) > 0:
                        top_k_tags = [self.vocabulary[index]
                                      for index in filter_indexes]
                    else:
                        top_k_tags = []
                    result.append({id_col: _id.item(), "tags": top_k_tags})

        result_ds = Dataset.from_dict(
            {key: [d[key] for d in result] for key in result[0]})
        return result_ds


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

    # Vocab variables
    args.add_argument('--dataset_vocab', type=str,
                      default='Multimodal-Fatima/descriptors-text-davinci-003')
    args.add_argument('--split_vocab', type=str, default='full')

    # Model variables
    args.add_argument('--vision_encoder_name',
                      required=True,
                      type=str,
                      default='openai/clip-vit-large-patch14')

    args.add_argument('--zeroshot_weights',
                      required=True,
                      type=str,
                      default='weights/attributes_clip/zw_attributes_laion_ViT_H_14_2B_descriptors_text_davinci_003_full.pt')

    # Parameters
    args.add_argument('--batch_size',
                      type=int,
                      default=8)

    args.add_argument('--num_workers',
                      type=int,
                      default=0)

    args.add_argument('--top_k',
                      type=int,
                      default=5)
    args.add_argument('--contrastive_th',
                      type=float,
                      default=0.2)
    args = args.parse_args()
    return args


def main():
    num_tasks = int(os.environ["WORLD_SIZE"])
    global_rank = int(os.environ["RANK"])
    local_rank = int(os.environ["LOCAL_RANK"])

    args = parse_args()
    ds = load_dataset(args.dataset_name, split=args.dataset_split)
    tagger = Tagger(vision_encoder_name=args.vision_encoder_name,
                    dataset_vocab=args.dataset_vocab,
                    split_vocab=args.split_vocab,
                    zeroshot_weights=args.zeroshot_weights,
                    device=local_rank)
    result_ds = tagger.get_tags(ds,
                                image_col=args.image_col,
                                id_col=args.id_col,
                                top_k=args.top_k,
                                contrastive_th=args.contrastive_th,
                                batch_size=args.batch_size,
                                num_workers=args.num_workers,
                                distributed_sampling=True)

    # Save in pickle all embeddings
    os.makedirs(Path(__file__).parent /
                "attributes_clip_tmp_folder/", exist_ok=True)
    result = []
    for item in result_ds:
        result.append(item)
    joblib.dump(result, Path(__file__).parent /
                f"attributes_clip_tmp_folder/data_{global_rank}.json")
    dist.barrier()

    if is_main_process():
        result = []
        dict_tags = {}
        for rank in range(num_tasks):
            result_file = Path(__file__).parent / \
                f"attributes_clip_tmp_folder/data_{rank}.json"
            res = joblib.load(result_file)
            result += res

        for res in result:
            dict_tags[res[args.id_col]] = res['tags']

        try:
            ds = load_dataset(args.dataset_name,
                              split=args.dataset_split)
        except:
            ds = load_from_disk(args.dataset_name)
        visionencoder_name = DICT_CLIP_NAME[args.vision_encoder_name]
        datasetvocab_name = args.dataset_vocab.split('/')[1].replace('-', '_')
        ds = ds.map(lambda example: {f"Attributes_{visionencoder_name}_{datasetvocab_name}_{args.split_vocab}": dict_tags[example[args.id_col]]},
                    batched=False)
        if args.save_disk:
            ds.save_to_disk(f"{args.dataset_name}_tags")
            # remove
            shutil.rmtree(args.dataset_name)
            # rename file
            os.rename(f"{args.dataset_name}_tags", args.dataset_name)
        else:
            ds.push_to_hub(args.dataset_name)


if __name__ == "__main__":
    ddp_setup()
    main()
    destroy_process_group()
