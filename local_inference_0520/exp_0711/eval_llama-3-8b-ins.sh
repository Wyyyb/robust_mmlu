#!/bin/bash

ngpu=4
save_dir="eval_results_0711/"
global_record_file="eval_results_0711/eval_record_collection_0711.csv"
model="/mnt/tjena/shared/Meta-Llama-3-8B-Instruct"
selected_subjects="all"
gpu_util=0.8
batch_size=2048
dataset="mmlu-pro"

cd ../
export CUDA_VISIBLE_DEVICES=3,4,5,6

python evaluate_from_local.py \
                 --selected_subjects $selected_subjects \
                 --ngpu $ngpu \
                 --save_dir $save_dir \
                 --model $model \
                 --global_record_file $global_record_file \
                 --gpu_util $gpu_util \
                 --batch_size $batch_size \
                 --dataset $dataset





