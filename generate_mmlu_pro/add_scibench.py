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


scibench_map = {
    "scibench-atkins.csv": "chemistry.csv",
    "scibench-chemmc.csv": "chemistry.csv",
    "scibench-class.csv": "physics.csv",
    "scibench-calculus.csv": "math.csv",
    "scibench-diff.csv": "math.csv",
    "scibench-fund.csv": "physics.csv",
    "scibench-matter.csv": "chemistry.csv",
    "scibench-quan.csv": "chemistry.csv",
    "scibench-stat.csv": "math.csv",
    "scibench-thermo.csv": "physics.csv"}


scibench_list = ["chemistry.csv", "math.csv", "physics.csv"]

output_dir = "../experiments/data/add_scibench_mmlu"
scibench_dir = "../experiments/data/mcq_scibench"
exist_mmlu_dir = "../experiments/data/add_theoremQA_mmlu"

os.makedirs(output_dir, exist_ok=True)

scibench_data_map = {}

for file in os.listdir(exist_mmlu_dir):
    if file.endswith("csv") and file not in scibench_list:
        data = read_csv_file(os.path.join(exist_mmlu_dir, file))
        write_2dlist_to_csv(data, os.path.join(output_dir, file))
    elif file.endswith("csv") and file in scibench_list:
        data = read_csv_file(os.path.join(exist_mmlu_dir, file))
        scibench_data_map[file] = data


for file in os.listdir(scibench_dir):
    if not file.startswith("scibench-"):
        continue
    file_path = os.path.join(scibench_dir, file)
    data = read_csv_file(file_path)
    for i, row in enumerate(data):
        data[i].append(file.replace(".csv", ""))
    if file not in scibench_map:
        print("file not in scibench_map")
        continue
    ori_data = scibench_data_map[scibench_map[file]]
    data = ori_data + data
    scibench_data_map[scibench_map[file]] = data
    # random.shuffle(data)

for file in scibench_list:
    data = scibench_data_map[file]
    write_2dlist_to_csv(data, os.path.join(output_dir, file))
    print(file, len(data))

