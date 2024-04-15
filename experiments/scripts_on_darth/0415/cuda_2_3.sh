#!/bin/bash

# 设置默认参数
ntrain=5
ngpu=2
data_dir="../data/mmlu_pro_4_options"
save_dir="../eval_result_0415"
options_num=4
use_rare_symbol=False
fixed_question_answer=-1
scoring_method="symbol_scoring"
model="meta-llama/Llama-2-13b-hf"

cd ../../../mmlu_pro_eval/
export CUDA_VISIBLE_DEVICES=5,6
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

use_rare_symbol=True
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

use_rare_symbol=False
fixed_question_answer=0
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

fixed_question_answer=1
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


fixed_question_answer=2
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

fixed_question_answer=3
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



                                