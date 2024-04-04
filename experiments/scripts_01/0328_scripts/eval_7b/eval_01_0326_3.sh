
cd ../eval
export CUDA_VISIBLE_DEVICES=3
python my_evaluate_llama.py -k 5 -g 1 -d ../../generate_plausible_options/expand_10_mmlu_data -s ../eval_result/mmlu_fix_C_exp_10_7b -m /ML-A100/team/mm/zhangge/Llama-2-7b-hf -f 2 -o 10






