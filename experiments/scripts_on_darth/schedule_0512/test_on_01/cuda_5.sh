#!/bin/bash

ntrain=5
examples_start_index=0
ngpu=1
data_dir="../../data/mmlu_pro_v1_0506"
save_dir="../eval_result_0512"
scoring_method="symbol_scoring"
model="01-ai/Yi-6B"
selected_subjects="all"

cd ../../../mmlu_pro_eval/

export CUDA_VISIBLE_DEVICES=5

prompt_type=0
for prompt_format in $(seq 0 6); do
    echo "Running with prompt_type=${prompt_type} and prompt_format=${prompt_format}"
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

prompt_format=0
for prompt_type in $(seq 1 8); do
    echo "Running with prompt_type=${prompt_type} and prompt_format=${prompt_format}"
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

for prompt_type in $(seq 1 8); do
    for prompt_format in $(seq 1 6); do
        echo "Running with prompt_type=${prompt_type} and prompt_format=${prompt_format}"
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
