#!/bin/bash

# 设置默认参数
ntrain=5
examples_start_index=0
prompt_type=2
prompt_format=336
ngpu=1
data_dir="../../data/ori_mmlu_data_json"
data_dir_list=(
    "../../data/ori_mmlu_data_json"
    "../../data/mmlu_pro_v1_0506"
)
save_dir="../eval_result_0516_standard"
scoring_method="symbol_scoring"
# scoring_method="hybrid_scoring"
# model="/ML-A100/team/mm/zhangge/Llama-2-7b-hf"
model="/ML-A800/models/Mistral-7B-Instruct-v0.2"
selected_subjects="all"
global_record_file="../result_record/eval_record_collection_0516_standard.csv"

cd ../../../mmlu_pro_eval/
export CUDA_VISIBLE_DEVICES=3

for data_dir in "${data_dir_list[@]}"; do
    echo "Evaluating: $model on: $data_dir with prompt_format: $prompt_format and prompt_type: $prompt_type"
    python evaluate_mmlu_pro_0516_prompt.py \
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
                 --global_record_file $global_record_file
    done






