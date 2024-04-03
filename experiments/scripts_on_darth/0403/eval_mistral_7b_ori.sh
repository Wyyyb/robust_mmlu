cd ../../mmlu_pro_eval
export CUDA_VISIBLE_DEVICES=2
python evaluate_mmlu_pro.py -k 5 -g 1 -d ../../data/add_stemez_mmlu -s ../../eval_result/0403_darth_result/ori -m mistralai/Mixtral-8x7B-v0.1






