from datasets import load_dataset
from datasets import Dataset
import json
import os


def pull_data():
    dataset = load_dataset("TIGER-Lab/MMLU-Pro")
    test_data, val_data = [], []
    for each in dataset["test"]:
        test_data.append(each)
    for each in dataset["validation"]:
        val_data.append(each)
    sta_subjects = {}
    for each in dataset["test"]:
        if each["category"] not in sta_subjects:
            sta_subjects[each["category"]] = 0
        sta_subjects[each["category"]] += 1
    print(sta_subjects)
    # os.makedirs("local_0521/", exist_ok=True)
    # with open("local_0521/mmlu_pro_test_data.json", "w") as fo:
    #     fo.write(json.dumps(test_data))
    # with open("local_0521/mmlu_pro_val_data.json", "w") as fo:
    #     fo.write(json.dumps(val_data))
    return test_data, val_data


def update_data(data):
    return data


def push_data(data):
    test_data, val_data = data
    test_dataset = Dataset.from_list(test_data)
    val_dataset = Dataset.from_list(val_data)
    test_dataset.push_to_hub("TIGER-Lab/MMLU-Pro", split="test")
    val_dataset.push_to_hub("TIGER-Lab/MMLU-Pro", split="validation")


if __name__ == "__main__":
    hf_data = pull_data()



