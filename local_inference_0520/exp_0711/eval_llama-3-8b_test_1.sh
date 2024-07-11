#!/bin/bash

ngpu=4
save_dir="eval_results_0712/"
global_record_file="eval_results_0712/eval_record_collection_0712.csv"
model="/mnt/tjena/shared/Meta-Llama-3-8B"
# model="meta-llama/Meta-Llama-3-8B"
# model="/ML-A800/models/Meta-Llama-3-8B"
selected_subjects="all"
gpu_util=0.8
batch_size=2048
dataset="mmlu-pro"
prompt_file="cot_prompt_lib/test_prompt_0711.txt"

cd ../
export CUDA_VISIBLE_DEVICES=3,4,5,6

python evaluate_from_local_0711.py \
                 --selected_subjects $selected_subjects \
                 --ngpu $ngpu \
                 --save_dir $save_dir \
                 --model $model \
                 --global_record_file $global_record_file \
                 --gpu_util $gpu_util \
                 --batch_size $batch_size \
                 --dataset $dataset \
                 --prompt_file $prompt_file





