#!/bin/bash

# 设置默认参数
ntrain=5
examples_start_index=0
prompt_type=2
prompt_format=1000
ngpu=2
data_dir="../../data/mmlu_pro_v1_0506"
save_dir="../eval_result_0531_NonCoT"
scoring_method="symbol_scoring"
# scoring_method="hybrid_scoring"
# model="/ML-A100/team/mm/zhangge/Llama-2-7b-hf"
# model="/ML-A100/team/mm/zhangge/Llama-2-7b-hf"
model="/ML-A100/public/model/Meta-Llama-3-70B-Instruct"
selected_subjects="all"
global_record_file="../eval_result_0531_NonCoT/eval_record_collection_0531_NonCoT.csv"

cd ../../mmlu_pro_eval/
export CUDA_VISIBLE_DEVICES=2,3

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
                 --global_record_file $global_record_file &


