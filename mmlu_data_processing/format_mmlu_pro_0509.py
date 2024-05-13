import json
import random
import os
import csv
import re


def read_csv_file(file_path):
    with open(file_path, mode='r', encoding='utf-8') as file:
        csv_reader = csv.reader(file)
        data = list(csv_reader)
        if str(data[0][0]) == "0" and str(data[0][1]) == "1" and str(data[0][2]) == "2":
            data = data[1:]
    return data


def format_mmlu_pro():
    format_test_data()
    format_dev_data()


def format_test_data():
    global max_q_id
    dir_path = "data/mmlu_pro_v1_0506"
    test_data = {}
    for file in os.listdir(dir_path):
        file_path = os.path.join(dir_path, file)
        if not file.endswith(".json"):
            continue
        with open(file_path, "r") as fi:
            curr = json.load(fi)
            category = file.replace(".json", "")
            for i, each in enumerate(curr):
                max_q_id = max(max_q_id, each["q_id"])
                new = {"question_id": each["q_id"], "question": each["question"], "options": each["options"],
                       "answer": each["answer"], "answer_index": each["answer_index"],
                       "cot_content": "", "category": category, "src": each["src"]}
                curr[i] = new
            curr = sorted(curr, key=lambda x: x["question_id"])
            if file not in test_data:
                test_data[file] = curr

    output_dir = "../data/mmlu_pro_v1_0512/test"
    for k, v in test_data.items():
        output_path = os.path.join(output_dir, k.replace(".json", "_test.json"))
        with open(output_path, "w") as fo:
            fo.write(json.dumps(v))

    output_dir = "../data/mmlu_pro_v1_0512/val"
    for k, v in test_data.items():
        output_path = os.path.join(output_dir, k.replace(".json", "_val.json"))
        with open(output_path, "w") as fo:
            fo.write(json.dumps(v[:10]))


def postprocess(cot_content, answer_symbol):
    pattern = r'The answer is \(([A-Z])\)'
    target = "The answer is (" + answer_symbol + ")"
    res = re.sub(pattern, target, cot_content)
    return res


def format_dev_data():
    global max_q_id
    cot_data = {}
    data = read_csv_file("data/mmlu_pro-cot.csv")
    for each in data:
        cat = each[1]
        if cat not in cot_data:
            cot_data[cat] = []
        options = each[3: 13]
        temp = []
        for opt in options:
            if opt.replace(" ", "") == "N/A":
                continue
            else:
                temp.append(opt)
        options = temp
        cot_content = each[15]
        cot_content = postprocess(cot_content, each[13])
        curr = {"question": each[2], "options": options, "answer": each[14], "answer_symbol": each[13],
                "cot_content": cot_content, "ori_key": each[0]}
        cot_data[cat].append(curr)
    dev_data = {}
    for k, v in cot_data.items():
        category = k
        file_name = k + "_dev.json"
        curr = []
        for each in v:
            max_q_id += 1
            single = {"question_id": max_q_id, "question": each["question"], "options": each["options"],
                      "answer": each["answer_symbol"],
                      "answer_index": "ABCDEFGHIJ".index(each["answer_symbol"]),
                      "cot_content": each["cot_content"], "category": category, "src": "cot_lib-" + each["ori_key"]}
            curr.append(single)
        if file_name not in dev_data:
            dev_data[file_name] = curr

    output_dir = "../data/mmlu_pro_v1_0512/dev"
    for k, v in dev_data.items():
        output_path = os.path.join(output_dir, k)
        with open(output_path, "w") as fo:
            fo.write(json.dumps(v))


if __name__ == '__main__':
    max_q_id = -1
    format_mmlu_pro()

