#!/bin/bash

ngpu=4
save_dir="eval_results_0606/"
global_record_file="eval_results_0606/eval_record_collection_0606.csv"
model="bosonai/Higgs-Llama-3-70B"
# model_list=("microsoft/Phi-3-medium-4k-instruct")
selected_subjects="all"
gpu_util=0.8
batch_size=2048

cd ../
export CUDA_VISIBLE_DEVICES=4,5,6,7

python evaluate_from_local.py \
                 --selected_subjects $selected_subjects \
                 --ngpu $ngpu \
                 --save_dir $save_dir \
                 --model $model \
                 --global_record_file $global_record_file \
                 --gpu_util $gpu_util \
                 --batch_size $batch_size




