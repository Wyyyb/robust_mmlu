#!/bin/bash
#source /gpfs/public/research/miniconda3/bin/activate
#conda activate vllm
ngpu=1
save_dir="eval_results_1101/"
global_record_file="eval_results_1101/eval_record_collection_1101.csv"
model="/data/yubowang/models/Llama-3.2-1B"
selected_subjects="all"
gpu_util=0.8
batch_size=100
dataset="mmlu-pro"
export HF_HOME="/data/yubowang/hf_home"

cd ../
export CUDA_VISIBLE_DEVICES=6

python evaluate_from_local_0907.py \
                 --selected_subjects $selected_subjects \
                 --ngpu $ngpu \
                 --save_dir $save_dir \
                 --model $model \
                 --global_record_file $global_record_file \
                 --gpu_util $gpu_util \
                 --batch_size $batch_size \
                 --dataset $dataset





