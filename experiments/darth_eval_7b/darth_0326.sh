export CUDA_VISIBLE_DEVICES=0
cd ../eval
python my_evaluate_llama.py -k 5 -g 1 -d ../../generate_plausible_options/expand_10_mmlu_data -s ../eval_result/mmlu_exp_10 -m meta-llama/Llama-2-7b-hf -o 10

python my_evaluate_llama.py -k 5 -g 1 -d ../../generate_plausible_options/expand_10_mmlu_data -s ../eval_result/mmlu_rare_symbol_exp_10 -m meta-llama/Llama-2-7b-hf -r True -o 10

python my_evaluate_llama.py -k 5 -g 1 -d ../../generate_plausible_options/expand_10_mmlu_data -s ../eval_result/mmlu_fix_B_exp_10 -m meta-llama/Llama-2-7b-hf -f 1 -o 10


