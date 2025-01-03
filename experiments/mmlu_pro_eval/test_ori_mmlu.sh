#!/bin/bash

# 设置默认参数
ntrain=5
ngpu=1
data_dir="../data/ori_mmlu_data"
save_dir="../test_data/test_ori_mmlu"
options_num=4
use_rare_symbol=False
fixed_question_answer=-1
scoring_method="symbol_scoring"
# model="google/gemma-7b"
model="/ML-A100/team/mm/zhangge/Llama-2-7b-hf"

# cd ../../../mmlu_pro_eval/
export CUDA_VISIBLE_DEVICES=7
# 调用 Python 脚本，并传递参数
python evaluate_mmlu_pro.py \
                 --ntrain $ntrain \
                 --ngpu $ngpu \
                 --data_dir $data_dir \
                 --save_dir $save_dir \
                 --options_num $options_num \
                 --use_rare_symbol $use_rare_symbol \
                 --fixed_question_answer $fixed_question_answer \
                 --scoring_method $scoring_method \
                 --model $model