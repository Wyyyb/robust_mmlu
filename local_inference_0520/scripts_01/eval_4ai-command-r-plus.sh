#!/bin/bash

ngpu=4
save_dir="eval_results_0604/"
global_record_file="eval_results_0604/eval_record_collection_0604.csv"
model="CohereForAI/c4ai-command-r-plus"
# model_list=("microsoft/Phi-3-medium-4k-instruct")
selected_subjects="all"
gpu_util=0.8
batch_size=2048

cd ../
export CUDA_VISIBLE_DEVICES=2,3,6,7

python evaluate_from_local.py \
                 --selected_subjects $selected_subjects \
                 --ngpu $ngpu \
                 --save_dir $save_dir \
                 --model $model \
                 --global_record_file $global_record_file \
                 --gpu_util $gpu_util \
                 --batch_size $batch_size





