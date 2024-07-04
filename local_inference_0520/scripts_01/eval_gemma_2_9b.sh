#!/bin/bash

ngpu=3
save_dir="eval_results_0703/"
global_record_file="eval_results_0703/eval_record_collection_0703.csv"
model="google/gemma-2-9b"
# model_list=("microsoft/Phi-3-medium-4k-instruct")
selected_subjects="all"
gpu_util=0.8
batch_size=2048

cd ../
export CUDA_VISIBLE_DEVICES=2,3,6
# export HF_HOME=/ML-A100/public/tmp

python evaluate_from_local.py \
                 --selected_subjects $selected_subjects \
                 --ngpu $ngpu \
                 --save_dir $save_dir \
                 --model $model \
                 --global_record_file $global_record_file \
                 --gpu_util $gpu_util \
                 --batch_size $batch_size


# model="/ML-A800/models/gemma-2-9b-it"
model="google/gemma-2-9b-it"

python evaluate_from_local.py \
                 --selected_subjects $selected_subjects \
                 --ngpu $ngpu \
                 --save_dir $save_dir \
                 --model $model \
                 --global_record_file $global_record_file \
                 --gpu_util $gpu_util \
                 --batch_size $batch_size

