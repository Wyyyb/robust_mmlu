#!/bin/bash

ngpu=1
save_dir="eval_results_0520/"
global_record_file="eval_results_0520/eval_record_collection_0520.csv"
# model="/ML-A100/team/mm/zhangge/Meta-Llama-3-70B-Instruct"
model_list=(
    "/ML-A800/models/Qwen1.5-7B-Chat"
    "/ML-A800/models/Qwen1.5-14B-Chat"
    "/ML-A800/models/Yi-6b-Chat"
    "/ML-A800/models/Yi-9B"
    "/ML-A800/models/Meta-Llama-3-8B"
    "/ML-A800/models/Meta-Llama-3-8B-Instruct"
    "/ML-A800/models/Llama-2-13b-hf"
    "/ML-A800/models/Llama-2-7b-hf"
    "/ML-A800/models/Mistral-7B-v0.1"
    "/ML-A800/models/Mistral-7B-Instruct-v0.1"
    "/ML-A800/models/Mistral-7B-Instruct-v0.2"
    "/ML-A800/models/Mistral-7B-v0.2-hf"
    "/ML-A800/models/gemma-7b"
    "/ML-A800/models/Yi-6B"
)
selected_subjects="all"
gpu_util=0.8
batch_size=2048

cd ../
export CUDA_VISIBLE_DEVICES=4

for model in "${model_list[@]}"; do
    python evaluate_from_local.py \
                 --selected_subjects $selected_subjects \
                 --ngpu $ngpu \
                 --save_dir $save_dir \
                 --model $model \
                 --global_record_file $global_record_file \
                 --gpu_util $gpu_util \
                 --batch_size $batch_size
done




