
cd ../eval
export CUDA_VISIBLE_DEVICES=2
python my_evaluate_llama.py -k 5 -g 1 -d ../../generate_plausible_options/expand_10_mmlu_data -s ../eval_result/mmlu_fix_B_exp_10_13b -m meta-llama/Llama-2-13b-hf -f 1 -o 10




