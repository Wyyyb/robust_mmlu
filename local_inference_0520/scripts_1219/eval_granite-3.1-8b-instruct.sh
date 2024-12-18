#!/bin/bash
source /gpfs/public/research/miniconda3/bin/activate
conda activate mmlu-pro
ngpu=1
save_dir="eval_results_1219/"
global_record_file="eval_results_1219/eval_record_collection_1219.csv"
model="/gpfs/public/research/models/granite-3.1-8b-instruct"
selected_subjects="all"
gpu_util=0.95
batch_size=100
dataset="mmlu-pro"
# export HF_HOME="/gpfs/public/research/xy/yubowang/hf_home"
export VLLM_ALLOW_LONG_MAX_MODEL_LEN=1

cd ../
export CUDA_VISIBLE_DEVICES=0

python evaluate_from_local_0711.py \
                 --selected_subjects $selected_subjects \
                 --ngpu $ngpu \
                 --save_dir $save_dir \
                 --model $model \
                 --global_record_file $global_record_file \
                 --gpu_util $gpu_util \
                 --batch_size $batch_size \
                 --dataset $dataset





