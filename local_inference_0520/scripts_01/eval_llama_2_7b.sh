#!/bin/bash

ngpu=1
save_dir="eval_results_0520/"
global_record_file="eval_results_0520/eval_record_collection_0520.csv"
model="/ML-A800/models/Llama-2-7b-hf"
selected_subjects="all"
gpu_util=0.8
batch_size=2048

cd ../
export CUDA_VISIBLE_DEVICES=0

python evaluate_from_local.py \
                 --selected_subjects $selected_subjects \
                 --ngpu $ngpu \
                 --save_dir $save_dir \
                 --model $model \
                 --global_record_file $global_record_file \
                 --gpu_util $gpu_util \
                 --batch_size $batch_size


