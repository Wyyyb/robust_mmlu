#!/bin/bash

# 设置默认参数
ntrain=5
examples_start_index=0
prompt_type=0
ngpu=1
# data_dir="../../data/ori_mmlu_data_json"
data_dir="../../data/mmlu_pro_v1_0506"
save_dir="../eval_result_0511"
# scoring_method="symbol_scoring"
scoring_method="hybrid_scoring"
# model="/ML-A100/team/mm/zhangge/Llama-2-7b-hf"
model="/ML-A100/team/mm/zhangge/Llama-2-7b-hf"
selected_subjects="physics"

cd ../../../mmlu_pro_eval/
export CUDA_VISIBLE_DEVICES=1

python evaluate_mmlu_pro_0511.py \
                 --ntrain $ntrain \
                 --examples_start_index $examples_start_index \
                 --prompt_type $prompt_type \
                 --selected_subjects $selected_subjects \
                 --ngpu $ngpu \
                 --data_dir $data_dir \
                 --save_dir $save_dir \
                 --scoring_method $scoring_method \
                 --model $model


prompt_type=1
python evaluate_mmlu_pro_0511.py \
                 --ntrain $ntrain \
                 --examples_start_index $examples_start_index \
                 --prompt_type $prompt_type \
                 --selected_subjects $selected_subjects \
                 --ngpu $ngpu \
                 --data_dir $data_dir \
                 --save_dir $save_dir \
                 --scoring_method $scoring_method \
                 --model $model

prompt_type=2
python evaluate_mmlu_pro_0511.py \
                 --ntrain $ntrain \
                 --examples_start_index $examples_start_index \
                 --prompt_type $prompt_type \
                 --selected_subjects $selected_subjects \
                 --ngpu $ngpu \
                 --data_dir $data_dir \
                 --save_dir $save_dir \
                 --scoring_method $scoring_method \
                 --model $model

prompt_type=3
python evaluate_mmlu_pro_0511.py \
                 --ntrain $ntrain \
                 --examples_start_index $examples_start_index \
                 --prompt_type $prompt_type \
                 --selected_subjects $selected_subjects \
                 --ngpu $ngpu \
                 --data_dir $data_dir \
                 --save_dir $save_dir \
                 --scoring_method $scoring_method \
                 --model $model

prompt_type=4
python evaluate_mmlu_pro_0511.py \
                 --ntrain $ntrain \
                 --examples_start_index $examples_start_index \
                 --prompt_type $prompt_type \
                 --selected_subjects $selected_subjects \
                 --ngpu $ngpu \
                 --data_dir $data_dir \
                 --save_dir $save_dir \
                 --scoring_method $scoring_method \
                 --model $model

prompt_type=5
python evaluate_mmlu_pro_0511.py \
                 --ntrain $ntrain \
                 --examples_start_index $examples_start_index \
                 --prompt_type $prompt_type \
                 --selected_subjects $selected_subjects \
                 --ngpu $ngpu \
                 --data_dir $data_dir \
                 --save_dir $save_dir \
                 --scoring_method $scoring_method \
                 --model $model



