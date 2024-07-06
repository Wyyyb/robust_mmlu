#!/bin/bash

ngpu=4
save_dir="eval_results_0706/"
global_record_file="eval_results_0706/eval_record_collection_0706.csv"
model="Qwen/Qwen2-72B-Instruct"
selected_subjects="all"
gpu_util=0.8
batch_size=2048

cd ../
export CUDA_VISIBLE_DEVICES=1,2,4,5
# export HF_HOME=/mnt/tjena/yubo/hf_home
export HF_HOME=/ML-A100/public/tmp

python evaluate_from_local.py \
                 --selected_subjects $selected_subjects \
                 --ngpu $ngpu \
                 --save_dir $save_dir \
                 --model $model \
                 --global_record_file $global_record_file \
                 --gpu_util $gpu_util \
                 --batch_size $batch_size


## model="/ML-A800/models/gemma-2-9b-it"
#model="Qwen/Qwen2-7B-Instruct"
#
#python evaluate_from_local.py \
#                 --selected_subjects $selected_subjects \
#                 --ngpu $ngpu \
#                 --save_dir $save_dir \
#                 --model $model \
#                 --global_record_file $global_record_file \
#                 --gpu_util $gpu_util \
#                 --batch_size $batch_size

