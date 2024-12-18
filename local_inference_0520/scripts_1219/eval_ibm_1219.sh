#!/bin/bash
source /gpfs/public/research/miniconda3/bin/activate
conda activate mmlu-pro

# 基础配置
ngpu=1
save_dir="eval_results_1219/"
global_record_file="eval_results_1219/eval_record_collection_1219.csv"
selected_subjects="all"
gpu_util=0.95
batch_size=100
dataset="mmlu-pro"
export VLLM_ALLOW_LONG_MAX_MODEL_LEN=1
export CUDA_VISIBLE_DEVICES=0

# 定义模型数组
models=(
    "/gpfs/public/research/models/granite-3.1-8b-instruct"
    "/gpfs/public/research/models/granite-3.1-8b-base"
    "/gpfs/public/research/models/granite-3.1-3b-a800m-instruct"
    "/gpfs/public/research/models/granite-3.1-3b-a800m-base"
    "/gpfs/public/research/models/granite-3.1-1b-a400m-instruct"
    "/gpfs/public/research/models/granite-3.1-1b-a400m-base"
    "/gpfs/public/research/models/granite-3.1-2b-instruct"
    "/gpfs/public/research/models/granite-3.1-2b-base"
)

# 创建保存目录
mkdir -p $save_dir

cd ../

# 循环执行每个模型的评估
for model_path in "${models[@]}"; do
    echo "正在评估模型: $model_path"

    python evaluate_from_local_0711.py \
        --selected_subjects $selected_subjects \
        --ngpu $ngpu \
        --save_dir $save_dir \
        --model $model_path \
        --global_record_file $global_record_file \
        --gpu_util $gpu_util \
        --batch_size $batch_size \
        --dataset $dataset

    echo "模型 $model_path 评估完成"
    echo "------------------------"
done

echo "所有模型评估完成"