#!/bin/bash

#source /xpfs/public/research/miniconda3/bin/activate
#conda activate lkg_eval

ngpu=4
save_dir="eval_results_0908/"
global_record_file="eval_results_0908/eval_record_collection_0908.csv"
model="/gpfs/public/research/xy/yubowang/models/Reflection-Llama-3.1-70B"
# model="meta-llama/Meta-Llama-3-8B"
# model="/ML-A800/models/Meta-Llama-3-8B"
selected_subjects="math"
gpu_util=0.8
batch_size=8
dataset="mmlu-pro"

cd ../
export CUDA_VISIBLE_DEVICES=0,1,2,3

python evaluate_from_local_0907.py \
                 --selected_subjects $selected_subjects \
                 --ngpu $ngpu \
                 --save_dir $save_dir \
                 --model $model \
                 --global_record_file $global_record_file \
                 --gpu_util $gpu_util \
                 --batch_size $batch_size \
                 --dataset $dataset \
                 --ntrain 0





