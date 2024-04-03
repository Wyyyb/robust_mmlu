cd ../../mmlu_pro_eval
export CUDA_VISIBLE_DEVICES=3
python evaluate_mmlu_pro_likelihood.py -k 5 -g 1 -d ../data/add_stemez_mmlu -s ../eval_result/0404_darth_result/hybrid_fixA -m meta-llama/Llama-2-7b-hf -q 0






