#!/bin/bash
#source /gpfs/public/research/miniconda3/bin/activate
#conda activate vllm
ngpu=4
save_dir="eval_results_1022/"
global_record_file="eval_results_1022/eval_record_collection_1022.csv"
model="mistralai/Mistral-Small-Instruct-2409"
selected_subjects="all"
gpu_util=0.8
batch_size=8
dataset="mmlu-pro"
export HF_HOME="/data/yubowang/hf_home"

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
                 --dataset $dataset





