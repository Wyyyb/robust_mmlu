cd ../../eval
export CUDA_VISIBLE_DEVICES=2
python my_evaluate_llama.py -k 5 -g 1 -d ../data/add_stemez_mmlu -s ../eval_result/0404_darth_result/ori_mmlu -m google/gemma-7b






