#!/bin/bash

ngpu=8
save_dir="eval_results_0920/"
global_record_file="eval_results_0920/eval_record_collection_0920.csv"
model="/mnt/tjena/yubo/models/"
selected_subjects="all"
gpu_util=0.8
batch_size=8
dataset="mmlu-pro"

cd ../
export CUDA_VISIBLE_DEVICES=0,1,2,3,4,5,6,7

python evaluate_from_local_0907.py \
                 --selected_subjects $selected_subjects \
                 --ngpu $ngpu \
                 --save_dir $save_dir \
                 --model $model \
                 --global_record_file $global_record_file \
                 --gpu_util $gpu_util \
                 --batch_size $batch_size \
                 --dataset $dataset





