import csv
import json
import os
import sys
from datasets import Dataset, DatasetDict
import random
from huggingface_hub import HfApi, HfFolder
from ori_mmlu_categories import ori_mmlu_subcategories, mmlu_pro_subcategories


removed_questions = ["Which of the following scans can image brain function?"]


def map_categories(ori_mmlu_cat):
    if ori_mmlu_cat not in ori_mmlu_subcategories:
        print("key error: ori_mmlu_cat")
        return None
    if ori_mmlu_subcategories[ori_mmlu_cat] not in mmlu_pro_subcategories:
        print("key error: ori_mmlu_subcategories[ori_mmlu_cat]")
        return None
    return mmlu_pro_subcategories[ori_mmlu_subcategories[ori_mmlu_cat]]


def read_csv_file(file_path):
    with open(file_path, mode='r', encoding='utf-8') as file:
        csv_reader = csv.reader(file)
        data = list(csv_reader)
        if str(data[0][0]) == "0" and str(data[0][1]) == "1" and str(data[0][2]) == "2":
            data = data[1:]
    return data


def write_2dlist_to_csv(data, file_name):
    with open(file_name, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerows(data)


def load_cot_data(cot_data_path, dataset, output_path):
    res = []
    if dataset == "mmlu_pro":
        option_num = 10
    else:
        option_num = 4
    q_id = 0
    mmlu_pro_dev = read_csv_file(cot_data_path)
    for each in mmlu_pro_dev:
        if len(each) != 6 + option_num:
            print("length wrong", len(each), each)
            continue
        src = f"cot_lib-{each[0]}"
        category = each[1]
        question = each[2]
        question_id = q_id
        q_id += 1
        options = each[3: 3 + option_num]
        answer = each[3 + option_num]
        answer_content = each[4 + option_num]
        answer_index = options.index(answer_content)
        map_str = "ABCDEFGHIJ"
        if map_str[answer_index] != answer:
            print("answer error", q_id, each)
            continue
        cot_content = each[5 + option_num]
        if dataset == "mmlu":
            category = map_categories(category)
        curr = {"question_id": question_id, "question": question, "options": options,
                "answer": answer, "answer_index": answer_index, "cot_content": cot_content,
                "category": category, "src": src}
        res.append(curr)
    res = check(res)
    with open(output_path, "w") as fo:
        fo.write(json.dumps(res))
    return res, q_id


def load_test_data(test_data_dir, dataset, output_path, start_q_id):
    res = []
    q_id = start_q_id
    for file in os.listdir(test_data_dir):
        file_path = os.path.join(test_data_dir, file)
        with open(file_path, "r") as fi:
            curr = json.load(fi)
            for i, each in enumerate(curr):
                curr[i]["question_id"] = q_id
                options = curr[i]["options"]
                if dataset == "mmlu_pro":
                    while len(options) < 10:
                        options.append("N/A")
                curr[i]["options"] = options
                if "q_id" in curr[i]:
                    curr[i].pop("q_id")
                q_id += 1
                if dataset == "mmlu":
                    curr[i]["cot_content"] = ""
                    curr[i]["category"] = map_categories(file.replace(".json", ""))
        res += curr
    res = check(res)
    with open(output_path, "w") as fo:
        fo.write(json.dumps(res))
    return res


def check(res):
    res = check_options(res)
    res = check_questions(res)
    return res


def check_questions(data_frame):
    res = []
    record = []
    for each in data_frame:
        question = each["question"]
        if question in removed_questions:
            continue
        answer_index = each["answer_index"]
        answer = each["options"][answer_index]
        question_id = question + answer
        if question_id not in record:
            res.append(each)
        else:
            print("repeated question", each)
    return res


def check_options(data_frame):
    option_duplicate_count = 0
    index_map = "ABCDEFGHIJ"
    res = []
    for each in data_frame:
        np = True
        res_options = []
        ori_options = each["options"]
        answer_index = each["answer_index"]
        answer = ori_options[answer_index]
        for opt in ori_options:
            if opt not in res_options or opt == "N/A":
                res_options.append(opt)
            else:
                np = False
                option_duplicate_count += 1
                print("\nduplicate options", opt)
                print("\nori data", each)
                print("option_duplicate_count", option_duplicate_count)
        if answer_index < len(res_options) and res_options[answer_index] == answer:
            pass
        else:
            print("answer index change from", each["answer_index"], res_options.index(answer))
            each["answer_index"] = res_options.index(answer)
            each["answer"] = index_map[each["answer_index"]]
        each["options"] = res_options
        res.append(each)
        if not np:
            print("\nnew data", each)
    return res


def format_data():
    mmlu_pro_cot_data, mmlu_pro_next_id = load_cot_data("input_data/mmlu_pro-cot.csv",
                                                        "mmlu_pro",
                                                        "../data/mmlu_pro_data_v1/mmlu_pro_dev.json")
    # mmlu_cot_data, mmlu_next_id = load_cot_data("input_data/ori_mmlu-cot.csv",
    #                                             "mmlu",
    #                                             "../data/ori_mmlu_data/ori_mmlu_dev.json")
    mmlu_pro_test_data = load_test_data("input_data/mmlu_pro_test/",
                                        "mmlu_pro",
                                        "../data/mmlu_pro_data_v1/mmlu_pro_test.json",
                                        mmlu_pro_next_id)
    # mmlu_test_data = load_test_data("input_data/ori_mmlu_data_json/",
    #                                 "mmlu",
    #                                 "../data/ori_mmlu_data/ori_mmlu_test.json",
    #                                 mmlu_next_id)
    push_to_hub(mmlu_pro_test_data, mmlu_pro_cot_data)
    # mmlu_pro_test_dataset = Dataset.from_list(mmlu_pro_test_data)
    # mmlu_pro_dev_dataset = Dataset.from_list(mmlu_pro_cot_data)
    # mmlu_pro_test_dataset.push_to_hub("TIGER-Lab/MMLU-Pro", private=True, split="test")
    # mmlu_pro_dev_dataset.push_to_hub("TIGER-Lab/MMLU-Pro", private=True, split="validation")


def push_to_hub(test_data, dev_data):
    subjects = {}
    for each in test_data:
        if each["category"] not in subjects:
            subjects[each["category"]] = []
        subjects[each["category"]].append(each)
    for k, v in subjects.items():
        sub_dataset = Dataset.from_list(v)
        sub_dataset.push_to_hub("TIGER-Lab/MMLU-Pro", k, split="test")
    # test_dataset = Dataset.from_list(test_data)
    # test_dataset.push_to_hub("TIGER-Lab/MMLU-Pro", "data", split="test")

    subjects = {}
    for each in dev_data:
        if each["category"] not in subjects:
            subjects[each["category"]] = []
        subjects[each["category"]].append(each)
    for k, v in subjects.items():
        sub_dataset = Dataset.from_list(v)
        sub_dataset.push_to_hub("TIGER-Lab/MMLU-Pro", k, split="validation")
    # dev_dataset = Dataset.from_list(dev_data)
    # dev_dataset.push_to_hub("TIGER-Lab/MMLU-Pro", "data", split="validation")


def update_to_hf():
    with open("../data/mmlu_pro_data_v1/mmlu_pro_test.json", "r") as fi:
        test_data = json.load(fi)
    test_dataset = Dataset.from_list(test_data)
    test_dataset.push_to_hub("TIGER-Lab/MMLU-Pro", split="test")

    with open("../data/mmlu_pro_data_v1/mmlu_pro_dev.json", "r") as fi:
        dev_data = json.load(fi)
    dev_dataset = Dataset.from_list(dev_data)
    dev_dataset.push_to_hub("TIGER-Lab/MMLU-Pro", split="validation")


if __name__ == '__main__':
    # format_data()
    update_to_hf()

