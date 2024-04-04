cd ../eval
export CUDA_VISIBLE_DEVICES=0
python my_evaluate_llama.py -k 5 -g 1 -d ../../generate_plausible_options/expand_10_mmlu_data -s ../eval_result/mmlu_exp_10_7b_chat -m /ML-A100/team/mm/zhangge/Llama-2-7b-chat-hf -o 10

cd ../eval
export CUDA_VISIBLE_DEVICES=1
python my_evaluate_llama.py -k 5 -g 1 -d ../../generate_plausible_options/expand_10_mmlu_data -s ../eval_result/mmlu_rare_symbol_exp_10_7b_chat -m /ML-A100/team/mm/zhangge/Llama-2-7b-chat-hf -r True -o 10

cd ../eval
export CUDA_VISIBLE_DEVICES=2
python my_evaluate_llama.py -k 5 -g 1 -d ../../generate_plausible_options/expand_10_mmlu_data -s ../eval_result/mmlu_fix_B_exp_10_7b_chat -m /ML-A100/team/mm/zhangge/Llama-2-7b-chat-hf -f 1 -o 10

cd ../eval
export CUDA_VISIBLE_DEVICES=3
python my_evaluate_llama.py -k 5 -g 1 -d ../../generate_plausible_options/expand_10_mmlu_data -s ../eval_result/mmlu_fix_C_exp_10_7b_chat -m /ML-A100/team/mm/zhangge/Llama-2-7b-chat-hf -f 2 -o 10

cd ../eval
export CUDA_VISIBLE_DEVICES=4
python my_evaluate_llama.py -k 5 -g 1 -d ../data/ori_mmlu_data -s ../eval_result/ori_mmlu_7b_chat -m /ML-A100/team/mm/zhangge/Llama-2-7b-chat-hf

cd ../eval
export CUDA_VISIBLE_DEVICES=5
python my_evaluate_llama.py -k 5 -g 1 -d ../data/ori_mmlu_data -s ../eval_result/ori_mmlu_7b_chat -m /ML-A100/team/mm/zhangge/Llama-2-7b-chat-hf -r True

cd ../eval
export CUDA_VISIBLE_DEVICES=6
python my_evaluate_llama.py -k 5 -g 1 -d ../data/ori_mmlu_data -s ../eval_result/ori_mmlu_7b_chat -m /ML-A100/team/mm/zhangge/Llama-2-7b-chat-hf -f 1

cd ../eval
export CUDA_VISIBLE_DEVICES=7
python my_evaluate_llama.py -k 5 -g 1 -d ../data/ori_mmlu_data -s ../eval_result/ori_mmlu_7b_chat -m /ML-A100/team/mm/zhangge/Llama-2-7b-chat-hf -f 2






