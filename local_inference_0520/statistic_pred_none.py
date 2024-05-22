import os
import json
import random


def func(input_dir):
    print("input_dir:", input_dir)
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
    hit_count = 0
    random_hit_count = 0
    for each in data:
        if not each["pred"]:
            pred_none_number += 1
            if each["answer"] == "A":
                hit_count += 1
            random.seed(12345)
            x = random.randint(0, len(each["options"]) - 1)
            if each["answer_index"] == x:
                random_hit_count += 1
    print("pred_none_number", pred_none_number)
    print("hit_count", hit_count)
    print("random_hit_count", random_hit_count)


if __name__ == "__main__":
    func("eval_results_0520/gemma-7b/CoT/all/")
    func("eval_results_0520/Qwen1.5-72B-Chat/CoT/all/")








