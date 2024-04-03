cd ../../mmlu_pro_eval
export CUDA_VISIBLE_DEVICES=1,2,3,4
python evaluate_mmlu_pro_likelihood.py -k 5 -g 4 -d ../data/add_stemez_mmlu -s ../eval_result/0404_darth_result/hybrid_ori -m mistralai/Mixtral-8x7B-v0.1






