import json
import os
import sys
from datasets import Dataset, DatasetDict
import random


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
    dataset_dict[subset_name] = {"test": transfer_list_to_ds(test_data),
                                 "validation": transfer_list_to_ds(dev_data)}
dataset_dict["all"] = {"test": transfer_list_to_ds(all_test),
                       "validation": transfer_list_to_ds(all_dev)}

for key, value in dataset_dict.items():
    for k, v in value.items():
        seg = key + "_" + k
        target = f"TIGER-Lab/MMLU-Pro"
        print("pushing to", target)
        v.push_to_hub(target, private=True)

# for subset, data in full_dataset.items():
#     data.push_to_hub(f"TIGER-Lab/MMLU-Pro/{subset}", private=False)







