import json
import os
import sys
from datasets import Dataset, DatasetDict
import random
from huggingface_hub import HfApi, HfFolder


def transfer_list_to_ds(list_data):
    res = {}
    for each in list_data:
        if each["question_id"] in res:
            print("repeated question id", each["question_id"])
            continue
        while len(each["options"]) < 10:
            each["options"].append("N/A")
        res[str(each["question_id"])] = each
    result = Dataset.from_dict(res)
    return result


api = HfApi()
username = api.whoami()['name']
token = HfFolder.get_token()
input_dir = "mmlu_pro_v1_0510"
dataset_dict = {}
all_subset = {}
all_test = []
all_dev = []
for dir_name in os.listdir(input_dir):
    dir_path = os.path.join(input_dir, dir_name)
    if not os.path.isdir(dir_path):
        continue
    subset_name = dir_name
    test_data_path = os.path.join(dir_path, subset_name + "_test.json")
    with open(test_data_path, "r") as fi:
        test_data = json.load(fi)
        all_test += test_data
    dev_data_path = os.path.join(dir_path, subset_name + "_dev.json")
    with open(dev_data_path, "r") as fi:
        dev_data = json.load(fi)
        all_dev += dev_data

dataset_test = Dataset.from_list(all_test)
dataset_dev = Dataset.from_list(all_dev)
dataset_test.push_to_hub("TIGER-Lab/MMLU-Pro", split="test")
dataset_dev.push_to_hub("TIGER-Lab/MMLU-Pro", split="validation")







