#!/bin/bash
#source /gpfs/public/research/miniconda3/bin/activate
#conda activate vllm
ngpu=1
save_dir="eval_results_1102/"
global_record_file="eval_results_1102/eval_record_collection_1102.csv"
model="/data/yubowang/models/SmolLM2-360M"
selected_subjects="all"
gpu_util=0.8
batch_size=100
dataset="mmlu-pro"
export HF_HOME="/data/yubowang/hf_home"
export VLLM_ALLOW_LONG_MAX_MODEL_LEN=1

cd ../
export CUDA_VISIBLE_DEVICES=1

python evaluate_from_local_0907.py \
                 --selected_subjects $selected_subjects \
                 --ngpu $ngpu \
                 --save_dir $save_dir \
                 --model $model \
                 --global_record_file $global_record_file \
                 --gpu_util $gpu_util \
                 --batch_size $batch_size \
                 --dataset $dataset





