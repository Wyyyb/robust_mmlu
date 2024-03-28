
cd ../eval
export CUDA_VISIBLE_DEVICES=7
python my_evaluate_llama.py -k 5 -g 1 -d ../data/ori_mmlu_data -s ../eval_result/ori_mmlu_13b_chat_fix_C -m meta-llama/Llama-2-13b-chat-hf -f 2






