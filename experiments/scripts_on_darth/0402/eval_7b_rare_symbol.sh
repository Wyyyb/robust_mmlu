cd ../../mmlu_pro_eval
export CUDA_VISIBLE_DEVICES=2
python evaluate_mmlu_pro.py -k 5 -g 1 -d ../../data/add_stemez_mmlu -s ../../eval_result/0402_darth_result/rare_symbol -m /ML-A100/team/mm/zhangge/Llama-2-7b-hf -r True






