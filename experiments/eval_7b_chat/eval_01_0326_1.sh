
cd ../eval
export CUDA_VISIBLE_DEVICES=1
python my_evaluate_llama.py -k 5 -g 1 -d ../../generate_plausible_options/expand_10_mmlu_data -s ../eval_result/mmlu_rare_symbol_exp_10_7b_chat -m meta-llama/Llama-2-7b-chat-hf -r True -o 10





