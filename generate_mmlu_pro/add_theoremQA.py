import csv
import os
import random


def read_csv_file(file_path):
    with open(file_path, mode='r', encoding='utf-8') as file:
        csv_reader = csv.reader(file)
        data = list(csv_reader)
    return data


def write_2dlist_to_csv(data, file_name):
    with open(file_name, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerows(data)


theorem_map = {
    "EECS_theoremQA_test.csv": "computer science.csv",
    "Finance_theoremQA_test.csv": "business.csv",
    "Math_theoremQA_test.csv": "math.csv",
    "Physics_theoremQA_test.csv": "physics.csv"}

theorem_list = ["computer science.csv", "business.csv", "math.csv", "physics.csv"]

output_dir = "../experiments/data/add_theoremQA_mmlu"
theoremQA_dir = "/Users/server/MMLU/code/mmlu_proj/trans_theorem/data/theoremQA"
exist_mmlu_dir = "../experiments/data/trim_down_mmlu"

os.makedirs(output_dir, exist_ok=True)

for file in os.listdir(exist_mmlu_dir):
    if file.endswith("csv") and file not in theorem_list:
        data = read_csv_file(os.path.join(exist_mmlu_dir, file))
        write_2dlist_to_csv(data, os.path.join(output_dir, file))


for file in os.listdir(theoremQA_dir):
    if not file.endswith("_theoremQA_test.csv"):
        continue
    file_path = os.path.join(theoremQA_dir, file)
    data = read_csv_file(file_path)
    for i, row in enumerate(data):
        data[i].append("theoremQA-" + file.replace("_theoremQA_test.csv", ""))
    if file not in theorem_map:
        print("file not in theorem_map")
        continue
    ori_data = read_csv_file(os.path.join(exist_mmlu_dir, theorem_map[file]))
    data = ori_data + data
    # random.shuffle(data)
    write_2dlist_to_csv(data, os.path.join(output_dir, theorem_map[file]))
    print(theorem_map[file], len(ori_data), len(data) - len(ori_data), len(data))












