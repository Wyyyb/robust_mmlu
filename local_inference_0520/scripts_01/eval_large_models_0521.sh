#!/bin/bash

ngpu=4
save_dir="eval_results_0521/"
global_record_file="eval_results_0521/eval_record_collection_0521.csv"
# model="/ML-A100/team/mm/zhangge/Llama-3-70B-Instruct"
model_list=(
    "/ML-A100/team/mm/zhangge/models/Qwen1.5-110B-Chat"
    "/ML-A100/team/mm/zhangge/models/Qwen1.5-72B"
    "/ML-A100/team/mm/zhangge/models/Qwen1.5-32B-Chat"
    "/ML-A100/team/mm/zhangge/models/Qwen1.5-32B"
    "/ML-A100/team/mm/zhangge/models/Yi-1.5-34B-Chat"
    "/ML-A100/team/mm/zhangge/models/Yi-1.5-9B-Chatt"
    "/ML-A100/team/mm/zhangge/models/Yi-1.5-6B-Chat"
)
selected_subjects="all"
gpu_util=0.8
batch_size=2048

cd ../
export CUDA_VISIBLE_DEVICES=0,1,2,3

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




