#!/bin/bash

# 设置默认参数
ntrain=5
examples_start_index=0
prompt_type=0
cot_type="cot_1"
ngpu=1
data_dir="../../data/mmlu_pro_v1_0506"
save_dir="../eval_result_0526"
use_rare_symbol=False
fixed_question_answer=-1
scoring_method="symbol_scoring"
# model="/ML-A100/team/mm/zhangge/Llama-2-7b-hf"
model="/ML-A100/team/mm/zhangge/models/OLMo-7B-Instruct"

cd ../../../mmlu_pro_eval/
export CUDA_VISIBLE_DEVICES=3
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