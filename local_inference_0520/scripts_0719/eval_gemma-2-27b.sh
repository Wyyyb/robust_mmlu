#!/bin/bash

ngpu=4
save_dir="eval_results_0730/"
global_record_file="eval_results_0730/eval_record_collection_0730.csv"
model="google/gemma-2-27b-it"
selected_subjects="all"
gpu_util=0.8
batch_size=2048
dataset="mmlu-pro"

cd ../
export CUDA_VISIBLE_DEVICES=2,3,4,5
export VLLM_ATTENTION_BACKEND=FLASHINFER

python evaluate_from_local.py \
                 --selected_subjects $selected_subjects \
                 --ngpu $ngpu \
                 --save_dir $save_dir \
                 --model $model \
                 --global_record_file $global_record_file \
                 --gpu_util $gpu_util \
                 --batch_size $batch_size \
                 --dataset $dataset

model="google/gemma-2-27b"

python evaluate_from_local.py \
                 --selected_subjects $selected_subjects \
                 --ngpu $ngpu \
                 --save_dir $save_dir \
                 --model $model \
                 --global_record_file $global_record_file \
                 --gpu_util $gpu_util \
                 --batch_size $batch_size \
                 --dataset $dataset

