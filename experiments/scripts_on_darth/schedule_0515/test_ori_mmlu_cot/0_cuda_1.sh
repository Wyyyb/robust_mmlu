#!/bin/bash

# 默认参数设置
ntrain=5
examples_start_index=0
prompt_type=8
prompt_format=0
ngpu=1
data_dir="../../data_formal/ori_mmlu_data"
save_dir="../eval_result_0515_ori_mmlu"
global_record_file="../result_record/eval_record_collection_0515_ori_mmlu.csv"
scoring_method="CoT"
selected_subjects="all"
batch_size=2048

# 模型列表
model_list=(
    "/ML-A100/team/mm/zhangge/Llama-2-7b-hf"
    "/ML-A100/team/mm/zhangge/Llama-2-13b-hf"
    "/ML-A800/models/Phi-3-mini-4k-instruct"
    "/ML-A800/models/Yi-6B"
    "/ML-A800/models/Meta-Llama-3-8B"
    "/ML-A800/models/Meta-Llama-3-8B-Instruct"
    "/ML-A800/models/Mistral-7B-Instruct-v0.2"
    "/ML-A800/models/Mistral-7B-v0.1"
)

cd ../../../mmlu_pro_eval/
export CUDA_VISIBLE_DEVICES=3
export VLLM_NO_USAGE_STATS=1

# 遍历模型列表并进行评估
for model in "${model_list[@]}"; do
    echo "Evaluating model: $model"
    python evaluate_mmlu_pro_cot_0513.py \
        --ntrain $ntrain \
        --examples_start_index $examples_start_index \
        --prompt_type $prompt_type \
        --prompt_format $prompt_format \
        --selected_subjects $selected_subjects \
        --ngpu $ngpu \
        --data_dir $data_dir \
        --save_dir $save_dir \
        --scoring_method $scoring_method \
        --model $model \
        --global_record_file $global_record_file \
        --batch_size $batch_size
done