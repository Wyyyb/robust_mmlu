#!/bin/bash
source /gpfs/public/research/miniconda3/bin/activate
conda activate mmlu-pro
ngpu=2
save_dir="eval_results_0127/"
global_record_file="eval_results_0127/eval_record_collection_0127.csv"
model="/gpfs/public/research/xy/yubowang/models/Sky-T1-32B-Preview"
selected_subjects="all"
gpu_util=0.95
batch_size=100
dataset="mmlu-pro"
# export HF_HOME="/gpfs/public/research/xy/yubowang/hf_home"
export VLLM_ALLOW_LONG_MAX_MODEL_LEN=1

cd ../
export CUDA_VISIBLE_DEVICES=0,1

python evaluate_from_local_0711.py \
                 --selected_subjects $selected_subjects \
                 --ngpu $ngpu \
                 --save_dir $save_dir \
                 --model $model \
                 --global_record_file $global_record_file \
                 --gpu_util $gpu_util \
                 --batch_size $batch_size \
                 --dataset $dataset





