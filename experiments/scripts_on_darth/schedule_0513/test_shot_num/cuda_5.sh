#!/bin/bash

# 设置默认参数
ntrain=5
examples_start_index=0
prompt_type=0
prompt_format=0
ngpu=1
data_dir="../../data/mmlu_pro_v1_0506"
save_dir="../eval_result_0513"
scoring_method="symbol_scoring"
# scoring_method="hybrid_scoring"
# model="/ML-A100/team/mm/zhangge/Llama-2-7b-hf"
model="meta-llama/Llama-2-7b-hf"
selected_subjects="all"

cd ../../../mmlu_pro_eval/
export CUDA_VISIBLE_DEVICES=0
prompt_format=0

for prompt_type in $(seq 0 6); do
    for ntrain in $(seq 3 5); do
        echo "Running with prompt_type=${prompt_type} and ntrain=${ntrain}"
        python evaluate_mmlu_pro_0511.py \
                         --ntrain $ntrain \
                         --examples_start_index $examples_start_index \
                         --prompt_type $prompt_type \
                         --prompt_format $prompt_format \
                         --selected_subjects $selected_subjects \
                         --ngpu $ngpu \
                         --data_dir $data_dir \
                         --save_dir $save_dir \
                         --scoring_method $scoring_method \
                         --model $model
    done
done
