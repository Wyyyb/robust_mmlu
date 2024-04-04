#!/bin/bash

#SBATCH --job-name=test_evaluate_llama
#SBATCH --output=eval-%j.out
#SBATCH --error=eval-%j.err
#SBATCH --partition=JIMMY
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --gres=gpu:1
#SBATCH --mem=4G
#SBATCH --time=01:00:00

# module load cuda/10.2  # 仅作示例，根据你的环境加载合适的模块
source activate robust_mmlu  # 激活你的 conda 环境

export CUDA_VISIBLE_DEVICES=0
cd ../eval/
python evaluate_llama.py -k 5 -g 1 -d ../test_data/test -s ../eval_result -m /ML-A100/team/mm/zhangge/Llama-2-7b-hf

