#!/bin/bash

# 设置默认参数
ntrain=5
examples_start_index=0
prompt_type=0
ngpu=1
data_dir="../../data/ori_mmlu_data_json"
save_dir="../eval_result_0508"
use_rare_symbol=False
fixed_question_answer=-1
scoring_method="hybrid_scoring"
model="01-ai/Yi-6B"

cd ../../../mmlu_pro_eval/
export CUDA_VISIBLE_DEVICES=4
# 调用 Python 脚本，并传递参数
python evaluate_mmlu_pro_json.py \
                 --ntrain $ntrain \
                 --examples_start_index $examples_start_index \
                 --prompt_type $prompt_type \
                 --ngpu $ngpu \
                 --data_dir $data_dir \
                 --save_dir $save_dir \
                 --use_rare_symbol $use_rare_symbol \
                 --fixed_question_answer $fixed_question_answer \
                 --scoring_method $scoring_method \
                 --model $model

prompt_type=1
python evaluate_mmlu_pro_json.py \
                 --ntrain $ntrain \
                 --examples_start_index $examples_start_index \
                 --prompt_type $prompt_type \
                 --ngpu $ngpu \
                 --data_dir $data_dir \
                 --save_dir $save_dir \
                 --use_rare_symbol $use_rare_symbol \
                 --fixed_question_answer $fixed_question_answer \
                 --scoring_method $scoring_method \
                 --model $model


examples_start_index=5
prompt_type=0
python evaluate_mmlu_pro_json.py \
                 --ntrain $ntrain \
                 --examples_start_index $examples_start_index \
                 --prompt_type $prompt_type \
                 --ngpu $ngpu \
                 --data_dir $data_dir \
                 --save_dir $save_dir \
                 --use_rare_symbol $use_rare_symbol \
                 --fixed_question_answer $fixed_question_answer \
                 --scoring_method $scoring_method \
                 --model $model


examples_start_index=0
prompt_type=0
fixed_question_answer=0
python evaluate_mmlu_pro_json.py \
                 --ntrain $ntrain \
                 --examples_start_index $examples_start_index \
                 --prompt_type $prompt_type \
                 --ngpu $ngpu \
                 --data_dir $data_dir \
                 --save_dir $save_dir \
                 --use_rare_symbol $use_rare_symbol \
                 --fixed_question_answer $fixed_question_answer \
                 --scoring_method $scoring_method \
                 --model $model

fixed_question_answer=1
python evaluate_mmlu_pro_json.py \
                 --ntrain $ntrain \
                 --examples_start_index $examples_start_index \
                 --prompt_type $prompt_type \
                 --ngpu $ngpu \
                 --data_dir $data_dir \
                 --save_dir $save_dir \
                 --use_rare_symbol $use_rare_symbol \
                 --fixed_question_answer $fixed_question_answer \
                 --scoring_method $scoring_method \
                 --model $model


fixed_question_answer=2
python evaluate_mmlu_pro_json.py \
                 --ntrain $ntrain \
                 --examples_start_index $examples_start_index \
                 --prompt_type $prompt_type \
                 --ngpu $ngpu \
                 --data_dir $data_dir \
                 --save_dir $save_dir \
                 --use_rare_symbol $use_rare_symbol \
                 --fixed_question_answer $fixed_question_answer \
                 --scoring_method $scoring_method \
                 --model $model

fixed_question_answer=3
python evaluate_mmlu_pro_json.py \
                 --ntrain $ntrain \
                 --examples_start_index $examples_start_index \
                 --prompt_type $prompt_type \
                 --ngpu $ngpu \
                 --data_dir $data_dir \
                 --save_dir $save_dir \
                 --use_rare_symbol $use_rare_symbol \
                 --fixed_question_answer $fixed_question_answer \
                 --scoring_method $scoring_method \
                 --model $model