# LENS🔍

## Intro

This is the repository for the CVasNLP project. Here, you can use our LENS (Language models ENhanced to See) system. First, the system runs a series of highly descriptive vision modules on your own dataset of images. These modules provide a large set of natural language captions, tags, objects, and attributes for each image. These natural language descriptions are then provided to a large language model (LLM) so that it can solve a variety of tasks relating to the image. Despite the simplicity of our system, and the fact that it requires no finetuning, we demonstrate in our paper that it often performs better than other SOTA image-language models such as FLAMINGO, CLIP, and KOSMOS.

### LENS for open ended visual question answering
![CVasNLP_open_ended_approach](https://github.com/ContextualAI/CVasNLP/assets/37418346/b3e13a70-e30f-42bd-9a17-506b79a2ce32)




### LENS for image classification
![CVasNLP_classification_approach](https://github.com/ContextualAI/CVasNLP/assets/37418346/d3909a16-339a-4194-88ea-d56bc8da536d)




## Setup

1. We reccomend that you get a machine with GPUs and CUDA.
   A machine with a single GPU or even only a CPU works,
   although for large datasets you should get several GPUs
   (and then modify batch_size, NPROCESS_PER_NODE, etc.
   in the command line section below so you can get faster inference).


2.  Create a python 3.9 conda environment and then install this repo as a pip package with:
    ```bash
    pip install llm-lens
    ```

## Python library usage

+ Attributes Tag Module
```python
from datasets import load_dataset
import lens.clip_attributes

ds = load_dataset("Multimodal-Fatima/cvasnlp_sample_test", split="test")

tagger = lens.clip_attributes.Tagger()

tags_ds = tagger.get_tags(ds)
```

+ Caption Module

```python
import lens.blip_captions

captioner = lens.blip_captions.Captioner()
captions_ds = captioner.get_captions(ds)
```

+ Intensive Caption Module

```python
intensive_captions_ds = captioner.get_intensive_captions(ds)
```

+ Pass the image descriptions from one of our dataset entries to a language model, and ask it a question

```python
from transformers import T5Tokenizer, T5ForConditionalGeneration

tokenizer = T5Tokenizer.from_pretrained("google/flan-t5-small")
model = T5ForConditionalGeneration.from_pretrained("google/flan-t5-small")

tags = '\n-'.join(tags_ds[0]["tags"])
intensive_captions = '\n'.join(intensive_captions_ds[0]["caption"])
caption = captions_ds[0]["caption"]
input_text = f"Captions:\n-{tags}\n-{intensive_captions}\n-{caption}"
input_text += "\nQuestion:What is in the image?"
input_text += "\nShort Answer:"
input_ids = tokenizer(input_text, return_tensors="pt").input_ids

outputs = model.generate(input_ids)
print(tokenizer.decode(outputs[0]))
```

## Examples of running the vision modules via command line scripts with multiple GPUs

To run these examples, clone this repo and then do a pip install from source:
```
git clone https://github.com/ContextualAI/lens.git
cd lens
pip install -e .
```

### Get or create a Hugging Face dataset that you want to use.

First, log into your Hugging Face acount:

```
huggingface-cli login
```

Now let's get our example dataset. The HF dataset  only needs to have an `image` and `id` column. Optionally, it can have a `label` column,
which contains the gold labels. The labels aren't used by the models - they are used by the evaluation
procedure at the end to compute metrics. A simple and correctly formatted example dataset can be found [here](https://huggingface.co/datasets/Multimodal-Fatima/cvasnlp_sample_test).
Feel free to open a python terminal and push this example dataset into your own HF account,
so you can quickly follow along with the rest of this README:
```
from datasets import load_dataset
ds = load_dataset("Multimodal-Fatima/cvasnlp_sample_test")
ds.push_to_hub("<your hf username>/cvasnlp_sample_test")
```

### Generate all the vision annotations that are going to be used

The following commands each add a new column to the Hugging Face dataset, with visual descriptions.
Each command pushes the dataset changes to the Hugging Face hub. Make sure to edit `DATASET` and `MASTER_ADDRESS` in the commands below before running them.

+ Attributes Tag Modules
    ```bash
    DATASET=<your hf username>/<your dataset name>
    SPLIT=test
    MASTER_ADDRESS=<ip of master; 'localhost' is fine if you are using a single node>
    MASTER_PORT=12345
    NPROCESS_PER_NODE=2
    VISION_ENCODER=hf-hub:laion/CLIP-ViT-H-14-laion2B-s32B-b79K
    ZSHOT_WEIGHT=weights/attributes_clip/zw_attributes_laion_ViT_H_14_2B_descriptors_text_davinci_003_full.pt

    torchrun \
        --rdzv_backend=c10d \
        --rdzv_endpoint=$MASTER_ADDRESS:$MASTER_PORT\
        --nproc_per_node=$NPROCESS_PER_NODE \
        clip_attributes.py  --dataset_name "${DATASET}"\
                            --dataset_split "${SPLIT}"\
                            --vision_encoder_name "${VISION_ENCODER}"\
                            --zeroshot_weights "${ZSHOT_WEIGHT}"\
                            --batch_size 8\
                            --num_workers 0 

    VISION_ENCODER=openai/clip-vit-large-patch14
    ZSHOT_WEIGHT=../weights/tags_clip/zw_tags_ViT_L_14_vocab_with_openai_classes.pt

    torchrun \
        --rdzv_backend=c10d \
        --rdzv_endpoint=$MASTER_ADDRESS:$MASTER_PORT\
        --nproc_per_node=$NPROCESS_PER_NODE \
        clip_attributes.py  --dataset_name "${DATASET}"\
                      --dataset_split "${SPLIT}"\
                      --vision_encoder_name "${VISION_ENCODER}"\
                      --zeroshot_weights "${ZSHOT_WEIGHT}"\
                      --batch_size 8\
                      --num_workers 0\
                      --dataset_vocab "../create_vocabs/objects/files/vocab_with_openai_classes.json"
    ```


+ Caption Module
    ```bash
    DATASET=<your hf username>/<your dataset name>
    SPLIT=test
    MASTER_ADDRESS=<ip of master; 'localhost' is fine if you are using a single node>
    MASTER_PORT=12345
    NPROCESS_PER_NODE=2

    torchrun \
        --rdzv_backend=c10d \
        --rdzv_endpoint=$MASTER_ADDRESS:$MASTER_PORT\
        --nproc_per_node=$NPROCESS_PER_NODE \
        blip_captions.py  --dataset_name "${DATASET}"\
                         --dataset_split "${SPLIT}"\
                         --model_name "Salesforce/blip-image-captioning-large"\
                         --num_beams 5\
                         --batch_size 8\
                         --num_workers 0
    ```
+ Intensive Caption Module
    ```bash
    DATASET=<your hf username>/<your dataset name>
    SPLIT=test
    MASTER_ADDRESS=<ip of master; 'localhost' is fine if you are using a single node>
    MASTER_PORT=12345
    NPROCESS_PER_NODE=2

    torchrun \
        --rdzv_backend=c10d \
        --rdzv_endpoint=$MASTER_ADDRESS:$MASTER_PORT\
        --nproc_per_node=$NPROCESS_PER_NODE \
        blip_captions.py  --dataset_name "${DATASET}"\
                                   --dataset_split "${SPLIT}"\
                                   --model_name "Salesforce/blip-image-captioning-large"\
				   --intensive\
                                   --load_8bit\
                                   --top_k 50\
                                   --num_captions 100\
                                   --batch_size 8\
                                   --num_workers 0
    ```
    

## Run LLMs on the vision model outputs and compute metrics

+ Evaluation
    ```bash
    cd evaluation
    DATASET=<your hf username>/<your dataset name>
    SPLIT=test
    MASTER_ADDRESS=<ip of master; 'localhost' is fine if you are using a single node>
    MASTER_PORT=12345
    NPROCESS_PER_NODE=2
    TYPE_EVALUATION=close-ended
    MODEL_CONFIG=configs/flan_small.yaml
    TEMPLATE_FORMAT="T|A"
    echo $TEMPLATE_FORMAT
    torchrun \
        --rdzv_backend=c10d \
        --rdzv_endpoint=$MASTER_ADDRESS:$MASTER_PORT\
        --nproc_per_node=$NPROCESS_PER_NODE \
        evaluation.py  --dataset_name "${DATASET}"\
                       --dataset_split "${SPLIT}"\
                       --type_evaluation "${TYPE_EVALUATION}"\
                       --config "${MODEL_CONFIG}"\
                       --template_format $TEMPLATE_FORMAT\
                       --metrics "accuracy,mean_per_class_accuracy"\
                       --load_8bit_acc "True"\
                       --tag_col "clip_tags_ViT_L_14_with_openai"\
                       --attribute_col "Attributes_LAION_ViT_H_14_2B_descriptors_text_davinci_003_full"\
                       --batch_size 8\
                       --mini_batch_size 16\
                       --num_workers 0
    ```

    Note: 
    - ```type_evaluation``` should be close-ended for Vision Classification tasks and open-ended for Vision and Language tasks
    - ```config```  include the model to be used and can be created in `evaluation/configs`
    - ```template_format``` refers to the vision modules to be included (`T`: Object Tags, `A`: Attribute tags, `CM`: Intensive Captioning module, `C`: global captioning module)
    - For the other variables, you can take a look at `evaluation/evaluation.py` script
    - This example showcases an image classification example. For open-ended tasks, like visual question answering, use `TYPE_EVALUATION=open-ended`. Unlike classification, visual question answering requires that you have a `question` column in your dataset.

## Citation

```
@inproceedings{berrios2022cvasnlp,
  author = {William Berrios and Gautam Mittal and Tristan Thrush and Moin Nadeem and Douwe Kiela and Amanpreet Singh},
  title = {Towards language models that can see: Computer vision through the lense of natural language},
  booktitle = {arXiv},
  year = 2023,
}
```
