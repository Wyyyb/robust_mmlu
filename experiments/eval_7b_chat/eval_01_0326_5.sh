
cd ../eval
export CUDA_VISIBLE_DEVICES=5
python my_evaluate_llama.py -k 5 -g 1 -d ../data/ori_mmlu_data -s ../eval_result/ori_mmlu_7b_chat_rare_symbol -m meta-llama/Llama-2-7b-chat-hf -r True




