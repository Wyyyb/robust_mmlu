import json
import csv
import re


input_file = "mmmu augmented sample - augmented_mmmu_sample.csv"


def read_csv_file(file_path):
    """
    This function reads a CSV file and returns the data as a list of rows.
    Each row is a list of values.

    :param file_path: The path to the CSV file to read.
    :return: A list of rows, where each row is a list of values.
    """
    with open(file_path, mode='r', encoding='utf-8') as file:
        csv_reader = csv.reader(file)
        # Skip the header if there is one
        # next(csv_reader, None)
        data = list(csv_reader)
    return data


def parse_options(response):
    res = []
    pattern = re.compile(r'^([E-J].).*')
    lines = response.split("\n")
    for line in lines:
        if pattern.match(line):
            res.append(line[2:].strip())
    if len(res) < 6:
        return None
    else:
        return res[:6]


with open("../human_check.json", "r") as fi:
    ori_data = json.load(fi)


result = []

csv_data = read_csv_file("mmmu augmented sample - augmented_mmmu_sample.csv")

csv_map = {}

for each in csv_data:
    q_id = each[0]
    if each[6] != "1":
        continue
    csv_map[q_id] = each[4]

for each in ori_data:
    if each["id"] not in csv_map:
        continue
    aug_opts = parse_options(csv_map[each["id"]])
    each["options"] += aug_opts
    result.append(each)

with open("augmented_mmmu_sample_0709.json", "w") as fo:
    fo.write(json.dumps(result, indent=2))




