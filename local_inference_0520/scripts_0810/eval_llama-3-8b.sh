#!/bin/bash

ngpu=1
model="/mnt/tjena/shared/Meta-Llama-3-8B"
# model="meta-llama/Meta-Llama-3-8B"
#model="/ML-A800/models/Meta-Llama-3-8B"
selected_subjects="all"
gpu_util=0.8
batch_size=2048
dataset="mmlu-pro"

cd ../
export CUDA_VISIBLE_DEVICES=4

for n_train in {0..4}
do
    save_dir="eval_results_0810_$n_train/"
    global_record_file="eval_results_0810/eval_record_collection_0810_$n_train.csv"

    python evaluate_from_local.py \
                     --ntrain "$n_train" \
                     --selected_subjects $selected_subjects \
                     --ngpu $ngpu \
                     --save_dir $save_dir \
                     --model $model \
                     --global_record_file $global_record_file \
                     --gpu_util $gpu_util \
                     --batch_size $batch_size \
                     --dataset $dataset
done