cd ../../mmlu_pro_eval
export CUDA_VISIBLE_DEVICES=4
python evaluate_mmlu_pro.py -k 5 -g 1 -d ../data/add_stemez_mmlu -s ../eval_result/0403_darth_result/fixB -m meta-llama/Llama-2-13b-hf -q 1





