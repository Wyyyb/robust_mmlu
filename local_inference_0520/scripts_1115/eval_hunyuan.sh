#!/bin/bash
source /gpfs/public/research/miniconda3/bin/activate
conda activate mmlu-pro
ngpu=8
save_dir="eval_results_1115/"
global_record_file="eval_results_1115/eval_record_collection_1115.csv"
model="/gpfs/public/research/xy/yubowang/models/Tencent-Hunyuan-Large/Hunyuan-A52B-Instruct"
selected_subjects="all"
gpu_util=0.8
batch_size=100
dataset="mmlu-pro"
export HF_HOME="/gpfs/public/research/xy/yubowang/hf_home"
export VLLM_ALLOW_LONG_MAX_MODEL_LEN=1

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




