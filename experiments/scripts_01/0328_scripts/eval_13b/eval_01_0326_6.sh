
cd ../eval
export CUDA_VISIBLE_DEVICES=6
python my_evaluate_llama.py -k 5 -g 1 -d ../data/ori_mmlu_data -s ../eval_result/ori_mmlu_13b_fix_B -m /ML-A100/team/mm/zhangge/Llama-2-13b-hf -f 1





