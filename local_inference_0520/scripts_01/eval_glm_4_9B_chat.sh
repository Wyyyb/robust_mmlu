#!/bin/bash

ngpu=1
save_dir="eval_results_0605/"
global_record_file="eval_results_0605/eval_record_collection_0605.csv"
model="THUDM/glm-4-9b-chat"
# model_list=("microsoft/Phi-3-medium-4k-instruct")
selected_subjects="all"
gpu_util=0.7
batch_size=2048

cd ../
export CUDA_VISIBLE_DEVICES=4

python evaluate_from_local.py \
                 --selected_subjects $selected_subjects \
                 --ngpu $ngpu \
                 --save_dir $save_dir \
                 --model $model \
                 --global_record_file $global_record_file \
                 --gpu_util $gpu_util \
                 --batch_size $batch_size





