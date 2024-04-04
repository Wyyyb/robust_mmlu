cd ../eval
export CUDA_VISIBLE_DEVICES=0
python my_evaluate_llama.py -k 5 -g 1 -d ../../generate_plausible_options/expand_10_mmlu_data -s ../eval_result/mmlu_exp_10_13b_chat -m /ML-A100/team/mm/zhangge/Llama-2-13b-chat-hf -o 10






