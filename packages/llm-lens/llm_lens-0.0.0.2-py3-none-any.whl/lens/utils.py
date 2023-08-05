from torch.distributed import init_process_group
import torch
import os
import datetime


default_device = "cuda" if torch.cuda.is_available() else "cpu"


def ddp_setup(): 
    init_process_group(backend="nccl",timeout=datetime.timedelta(seconds=180000))
    torch.cuda.set_device(int(os.environ["LOCAL_RANK"]))


def create_sampler(dataset, distributed=False):
    if distributed:
        sampler = torch.utils.data.DistributedSampler(dataset,shuffle=False)
    else:
        sampler = torch.utils.data.SequentialSampler(dataset)
    return sampler 


def create_dataloader(dataset,sampler, batch_size=8, num_workers=0):
    loader = torch.utils.data.DataLoader(
            dataset,
            batch_size=batch_size,
            num_workers= num_workers,
            pin_memory=True,
            sampler = sampler,
            shuffle= False,
            drop_last= False,
        )              
    return loader


def is_main_process():
    if int(os.environ["RANK"])==0:
        return True
    else:
        return False
