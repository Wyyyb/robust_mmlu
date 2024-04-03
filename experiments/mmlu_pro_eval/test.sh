export CUDA_VISIBLE_DEVICES=0,1,2,3,4,5,6,7
python evaluate_mmlu_pro.py -k 5 -g 8 -d ../data/add_stemez_mmlu -s ../eval_result/0404_darth_result/hybrid_ori -m mistralai/Mixtral-8x7B-v0.1






