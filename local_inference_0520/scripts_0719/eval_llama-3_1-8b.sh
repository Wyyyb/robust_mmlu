#!/bin/bash

ngpu=2
save_dir="eval_results_0729/"
global_record_file="eval_results_0729/eval_record_collection_0729.csv"
model="/mnt/tjena/yubo/models/Meta-Llama-3.1-8B"
# model="meta-llama/Meta-Llama-3-8B"
# model="/ML-A800/models/Meta-Llama-3-8B"
selected_subjects="all"
gpu_util=0.8
batch_size=2048
dataset="mmlu-pro"

cd ../
export CUDA_VISIBLE_DEVICES=2,3

python evaluate_from_local.py \
                 --selected_subjects $selected_subjects \
                 --ngpu $ngpu \
                 --save_dir $save_dir \
                 --model $model \
                 --global_record_file $global_record_file \
                 --gpu_util $gpu_util \
                 --batch_size $batch_size \
                 --dataset $dataset





