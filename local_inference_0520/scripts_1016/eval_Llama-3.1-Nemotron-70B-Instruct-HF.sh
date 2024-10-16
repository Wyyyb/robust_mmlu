#!/bin/bash
source /gpfs/public/research/miniconda3/bin/activate
conda activate vllm
ngpu=8
save_dir="eval_results_1016/"
global_record_file="eval_results_1016/eval_record_collection_1016.csv"
model="/gpfs/public/research/xy/yubowang/models/Llama-3.1-Nemotron-70B-Instruct-HF"
selected_subjects="all"
gpu_util=0.8
batch_size=-1
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





