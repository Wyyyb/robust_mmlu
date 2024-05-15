import csv
import json
import argparse
import os
import torch
import numpy as np
import random
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer, AutoModelForCausalLM, GenerationConfig
import transformers
import time
import re
from tqdm import tqdm
from distutils.util import strtobool
import logging
import sys
from prompt_format_examples import prompt_format_examples



def args_generate_path(input_args):
    scoring_method = input_args.scoring_method
    if args.cot_type != "-1":
        scoring_method = args.cot_type
    model_name = input_args.model.split("/")[-1]
    if "ori_mmlu" in input_args.data_dir:
        dataset_name = "mmlu"
    elif "mmlu_pro" in input_args.data_dir:
        dataset_name = "mmlu_pro"
    else:
        dataset_name = "mmlu"
    logging.info("dataset type", dataset_name)
    examples_start_index = f"es_{str(input_args.examples_start_index)}"
    prompt_type = f"prompt_{str(input_args.prompt_type)}"
    prompt_format = f"format_{str(input_args.prompt_format)}"
    res = f"{scoring_method}/{model_name}/{dataset_name}/{examples_start_index}/{prompt_type}/{prompt_format}"
    if args.selected_subjects != "all":
        res += "/" + args.selected_subjects.replace(",", "-").replace(" ", "_")
    return res


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ntrain", "-k", type=int, default=5)
    parser.add_argument("--examples_start_index", "-esi", type=int, default=0)
    parser.add_argument("--prompt_type", "-p", type=int, default=0)
    parser.add_argument("--prompt_format", "-pf", type=int, default=0)
    parser.add_argument("--selected_subjects", "-sub", type=str, default="all")
    parser.add_argument("--ngpu", "-g", type=int, default=1)
    parser.add_argument("--data_dir", "-d", type=str, default="data")
    parser.add_argument("--save_dir", "-s", type=str, default="results")
    parser.add_argument("--scoring_method", "-sm", type=str, default="symbol_scoring")
    parser.add_argument("--model", "-m", type=str, default="/ML-A100/team/mm/zhangge/Llama-2-7b-hf")
    global_record_file = "../experiments/result_record/eval_record_collection_0512.csv"
    os.makedirs("../result_record", exist_ok=True)
    args = parser.parse_args()

    save_result_dir = os.path.join(
        args.save_dir, args_generate_path(args)
    )
    file_prefix = args_generate_path(args).replace("/", "-")
    timestamp = time.time()
    time_str = time.strftime('%m-%d_%H-%M', time.localtime(timestamp))
    file_name = f"{file_prefix}_{time_str}_summary.txt"
    summary_path = os.path.join(args.save_dir, "summary", file_name)
    os.makedirs(os.path.join(args.save_dir, "summary"), exist_ok=True)
    os.makedirs(save_result_dir, exist_ok=True)
    save_log_dir = os.path.join(args.save_dir, "log")
    os.makedirs(save_log_dir, exist_ok=True)
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s %(message)s',
                        handlers=[logging.FileHandler(os.path.join(save_log_dir,
                                                                   file_name.replace("_summary.txt",
                                                                                     "_logfile.log"))),
                                  logging.StreamHandler(sys.stdout)])

    main()








