from datasets import load_dataset
from datasets import Dataset
import json


def push_data():
    with open("pushed_data/test_data.json", "r") as fi:
        test_data = json.load(fi)
    with open("pushed_data/mmlu_pro_val_data.json", "r") as fi:
        val_data = json.load(fi)
    for i, each in enumerate(test_data):
        if "cot_content" not in each:
            test_data[i]["cot_content"] = ""
    print("length of test_data", len(test_data))
    test_dataset = Dataset.from_list(test_data)
    val_dataset = Dataset.from_list(val_data)
    test_dataset.push_to_hub("TIGER-Lab/MMLU-Pro", split="test")
    val_dataset.push_to_hub("TIGER-Lab/MMLU-Pro", split="validation")


if __name__ == "__main__":
    push_data()



