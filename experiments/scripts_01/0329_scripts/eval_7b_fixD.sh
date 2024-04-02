cd ../eval
export CUDA_VISIBLE_DEVICES=7
python my_evaluate_llama.py -k 5 -g 1 -d ../data/add_stemez_mmlu -s ../eval_result/0402_darth_result -m meta-llama/Llama-2-7b-hf -q 3





