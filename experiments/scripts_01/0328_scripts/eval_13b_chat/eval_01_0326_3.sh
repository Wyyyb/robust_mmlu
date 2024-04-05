
cd ../eval
export CUDA_VISIBLE_DEVICES=3
python my_evaluate_llama.py -k 5 -g 1 -d ../../generate_plausible_options/expand_10_mmlu_data -s ../eval_result/mmlu_fix_C_exp_10_13b_chat -m meta-llama/Llama-2-13b-chat-hf -f 2 -o 10






