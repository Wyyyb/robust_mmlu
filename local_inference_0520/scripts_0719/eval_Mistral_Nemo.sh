#!/bin/bash

ngpu=4
save_dir="eval_results_0725/"
global_record_file="eval_results_0725/eval_record_collection_0725.csv"
# model="/ML-A100/team/mm/models/Mistral-Nemo-Instruct-2407"
model="mistralai/Mistral-Nemo-Instruct-2407"
# model="meta-llama/Meta-Llama-3-8B"
# model="/ML-A800/models/Meta-Llama-3-8B"
selected_subjects="all"
gpu_util=0.8
batch_size=2048
dataset="mmlu-pro"

cd ../
export CUDA_VISIBLE_DEVICES=4,5,6,7

python evaluate_from_local.py \
                 --selected_subjects $selected_subjects \
                 --ngpu $ngpu \
                 --save_dir $save_dir \
                 --model $model \
                 --global_record_file $global_record_file \
                 --gpu_util $gpu_util \
                 --batch_size $batch_size \
                 --dataset $dataset

# model="/ML-A100/team/mm/models/Mistral-Nemo-Base-2407"
model="mistralai/Mistral-Nemo-Base-2407"

python evaluate_from_local.py \
                 --selected_subjects $selected_subjects \
                 --ngpu $ngpu \
                 --save_dir $save_dir \
                 --model $model \
                 --global_record_file $global_record_file \
                 --gpu_util $gpu_util \
                 --batch_size $batch_size \
                 --dataset $dataset

