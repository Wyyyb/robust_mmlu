cd ../../mmlu_pro_eval
export CUDA_VISIBLE_DEVICES=6
python evaluate_mmlu_pro.py -k 5 -g 1 -d ../data/add_stemez_mmlu -s ../eval_result/0403_darth_result/fixC -m /ML-A100/team/mm/zhangge/Llama-2-7b-hf -q 2






