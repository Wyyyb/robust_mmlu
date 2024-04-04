
cd ../eval
export CUDA_VISIBLE_DEVICES=4
python my_evaluate_llama.py -k 5 -g 1 -d ../data/ori_mmlu_data -s ../eval_result/ori_mmlu_7b -m /ML-A100/team/mm/zhangge/Llama-2-7b-hf




