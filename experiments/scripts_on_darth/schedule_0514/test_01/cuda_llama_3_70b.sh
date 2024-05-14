#!/bin/bash

# 设置默认参数
ntrain=5
examples_start_index=0
prompt_type=8
prompt_format=0
ngpu=4
data_dir="../../data_formal/mmlu_pro_data_v1"
save_dir="../eval_result_0514_CoT"
global_record_file="../result_record/eval_record_collection_0514_01.csv"
# scoring_method="symbol_scoring"
scoring_method="CoT"
# model="/ML-A100/team/mm/zhangge/Llama-2-7b-hf"
model="/ML-A100/team/mm/zhangge/Meta-Llama-3-70B"
selected_subjects="all"
gpu_util="0.7"
batch_size=512

cd ../../../mmlu_pro_eval/
export CUDA_VISIBLE_DEVICES=0,2,4,5
export VLLM_NO_USAGE_STATS=1

python evaluate_mmlu_pro_cot_0513.py \
                 --ntrain $ntrain \
                 --examples_start_index $examples_start_index \
                 --prompt_type $prompt_type \
                 --prompt_format $prompt_format \
                 --selected_subjects $selected_subjects \
                 --ngpu $ngpu \
                 --gpu_util $gpu_util \
                 --data_dir $data_dir \
                 --save_dir $save_dir \
                 --scoring_method $scoring_method \
                 --model $model \
                 --global_record_file $global_record_file \
                 --batch_size $batch_size




