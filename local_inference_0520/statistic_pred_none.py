import os
import json


def func(input_dir):
    data = []
    for file in os.listdir(input_dir):
        if file.startswith("."):
            continue
        file_path = os.path.join(input_dir, file)
        with open(file_path, "r") as fi:
            curr = json.load(fi)
            data += curr
    print("length of data", len(data))
    pred_none_number = 0
    for each in data:
        if not each["pred"]:
            pred_none_number += 1
    print("pred_none_number", pred_none_number)


if __name__ == "__main__":
    func("eval_results_0520/gemma-7b/CoT/all/")
    func("eval_results_0520/Qwen1.5-72B-Chat/CoT/all/")








