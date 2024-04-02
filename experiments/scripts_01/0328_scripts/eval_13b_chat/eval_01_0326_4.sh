
cd ../eval
export CUDA_VISIBLE_DEVICES=4
python my_evaluate_llama.py -k 5 -g 1 -d ../data/ori_mmlu_data -s ../eval_result/ori_mmlu_13b_chat -m meta-llama/Llama-2-13b-chat-hf




