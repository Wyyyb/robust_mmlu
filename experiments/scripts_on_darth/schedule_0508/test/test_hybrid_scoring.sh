#!/bin/bash

# 设置默认参数
ntrain=5
examples_start_index=0
prompt_type=0
cot_type="-1"
ngpu=1
data_dir="../../data/mmlu_pro_v1_sample"
save_dir="../test_result_0508"
use_rare_symbol=False
fixed_question_answer=-1
scoring_method="hybrid_scoring"
model="/ML-A100/team/mm/zhangge/Llama-2-7b-hf"
# model="google/gemma-7b"

cd ../../../mmlu_pro_eval/
export CUDA_VISIBLE_DEVICES=0
# 调用 Python 脚本，并传递参数
python evaluate_mmlu_pro_json.py \
                 --ntrain $ntrain \
                 --examples_start_index $examples_start_index \
                 --prompt_type $prompt_type \
                 --cot_type $cot_type \
                 --ngpu $ngpu \
                 --data_dir $data_dir \
                 --save_dir $save_dir \
                 --use_rare_symbol $use_rare_symbol \
                 --fixed_question_answer $fixed_question_answer \
                 --scoring_method $scoring_method \
                 --model $model
