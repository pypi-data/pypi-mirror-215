from transformers import (
    set_seed,
    HfArgumentParser,
    TrainingArguments,
)
import argparse
from ray.train.huggingface import TransformersTrainer
from ray.air.config import ScalingConfig
from ray.data.preprocessors import Chain
import os
from os.path import join
import torch
from transformers import AutoTokenizer
from transformers import AutoModelForCausalLM
from ..sft.collator import SFTDataCollator
from ..sft.dataset import SFTDataset
from ..sft.argument import CustomizedArguments
from ..sft.trainer import Trainer
from ..sft.loss import TargetLMLoss


def setup_everything():
    parser = argparse.ArgumentParser()
    parser.add_argument("--train_args_file", type=str, default='train_args/finetune.json', help="")
    args = parser.parse_args()
    train_args_file = args.train_args_file
    # train_args_file = 'train_args/finetune.json'
    # 读取训练的参数配置
    parser = HfArgumentParser((CustomizedArguments, TrainingArguments))
    # 解析得到自定义参数，以及自带参数
    args, training_args = parser.parse_json_file(json_file=train_args_file)
    # 创建输出目录
    if not os.path.exists(training_args.output_dir):
        os.makedirs(training_args.output_dir)
    
    print("train_args:{}".format(training_args))
    # 设置随机种子
    set_seed(training_args.seed)
    return args, training_args


def trainer_init_per_worker(args, training_args):
    """
    初始化各个组件
    """
    print('Initializing components...')
    world_size = int(os.environ.get("WORLD_SIZE", 1))
    ddp = world_size != 1
    if ddp:
        device_map = {"": int(os.environ.get("LOCAL_RANK") or 0)}
    training_args.ddp_find_unused_parameters = False if ddp else None

    # 加载tokenzier
    tokenizer = AutoTokenizer.from_pretrained(
        args.model_name_or_path,
        trust_remote_code=True
    )
    # 初始化model
    model = AutoModelForCausalLM.from_pretrained(
        args.model_name_or_path,
        torch_dtype=torch.float16,
        trust_remote_code=True
    )
    # 计算模型参数量
    total = sum(p.numel() for p in model.parameters())
    print("Total model params: %.2fM" % (total / 1e6))

    # 初始化损失函数
    loss_func = TargetLMLoss(ignore_index=tokenizer.pad_token_id)
    # 加载训练集
    train_dataset = SFTDataset(args.train_file, tokenizer, args.max_seq_length)
    data_collator = SFTDataCollator(tokenizer, args.max_seq_length)

    # 初始化Trainer
    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=train_dataset,
        tokenizer=tokenizer,
        data_collator=data_collator,
        compute_loss=loss_func
    )
    trainer.train()


def train(num_workers:int,use_gpu:bool, cpus_per_worker:int):
    distribute_trainer = TransformersTrainer(
                                    trainer_init_per_worker=trainer_init_per_worker,
                                    trainer_init_config={
                                        "batch_size": 16,  # per device
                                        "epochs": 1,
                                    },
                                    scaling_config=ScalingConfig(
                                        num_workers=num_workers,
                                        use_gpu=use_gpu,
                                        resources_per_worker={"GPU": 1, "CPU": cpus_per_worker},
                                    ),
                                    
                                    datasets={"train": ray_datasets["train"], "evaluation": ray_datasets["validation"]},
                                    preprocessor=Chain(splitter, tokenizer),
    ) 
    distribute_trainer.fit()



   



