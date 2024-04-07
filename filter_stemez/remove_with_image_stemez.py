import csv
import os
import json


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


def load_stemez_meta_info():
    stemez_meta_info = {}
    for file in os.listdir(stemez_meta_info_dir):
        # print(file)
        if not file.endswith("jsonl"):
            continue
        file_path = os.path.join(stemez_meta_info_dir, file)
        with open(file_path, "r", encoding="utf-8") as fi:
            for line in fi.readlines():
                curr = json.loads(line)
                question = curr["question"]
                src = "stemez-" + file.split("_")[1]
                html = curr["html_file"]
                image_num = len(curr["images"])
                if src not in stemez_meta_info:
                    stemez_meta_info[src] = {}
                if question not in stemez_meta_info[src]:
                    stemez_meta_info[src][question] = []
                stemez_meta_info[src][question].append([image_num, html])
    return stemez_meta_info


def remove():
    human_check = []
    human_check_path = os.path.join(output_dir, "../human_check.csv")
    removed_question = []
    removed_questions_path = os.path.join(output_dir, "../removed_questions.csv")
    os.makedirs(output_dir, exist_ok=True)
    stemez_meta_info = load_stemez_meta_info()
    for file in os.listdir(input_dir):
        file_path = os.path.join(input_dir, file)
        output_path = os.path.join(output_dir, file)
        output_res = []
        data = read_csv_file(file_path)
        for each in data:
            src = each[6]
            question = each[0]
            if src not in stemez_meta_info:
                output_res.append(each)
                continue
            if question not in stemez_meta_info[src]:
                print("question not in stemez_meta_info[src]", question)
                continue
            if len(stemez_meta_info[src][question]) != 1:
                check = each + [file]
                human_check.append(check)
                continue
            image_num = stemez_meta_info[src][question][0][0]
            html = stemez_meta_info[src][question][0][1]
            if image_num > 0:
                removed = each + [file, html]
                removed_question.append(removed)
                continue
            output_res.append(each)
        write_2dlist_to_csv(output_res, output_path)
    write_2dlist_to_csv(human_check, human_check_path)
    write_2dlist_to_csv(removed_question, removed_questions_path)


input_dir = "../experiments/data/mmlu_pro_v1"
stemez_meta_info_dir = "/Users/server/MMLU/git/ScienceEval/mmlu_pro/processed_data"
output_dir = "data/images_removed_mmlu"

remove()



