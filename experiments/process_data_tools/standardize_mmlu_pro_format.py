import csv
import os
import pandas as pd


def save_to_csv_with_newlines(data, filename):
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        csvwriter = csv.writer(csvfile, escapechar='\\', doublequote=False, quoting=csv.QUOTE_ALL)
        # 将data写入CSV文件
        for item in data:
            # 确保每个条目是作为单个字段写入
            csvwriter.writerow(item)


def write_2dlist_to_csv(data, file_name):
    with open(file_name, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerows(data)


def read_csv_file(file_path):
    with open(file_path, mode='r', encoding='utf-8') as file:
        csv_reader = csv.reader(file)
        data = list(csv_reader)
    return data


def pandas_read_csv_file(file_path, start_line=0):
    if start_line == 1:
        df = pd.read_csv(file_path, header=0)
    else:
        df = pd.read_csv(file_path, header=None)
    data = df.values.tolist()
    return data


def standardize_mmlu_pro_format(input_dir, output_dir):
    mmlu_data = {}
    exist_questions = []
    subject_count = {}
    for file in os.listdir(input_dir):
        if not file.endswith(".csv"):
            continue
        curr_subject_data = []
        duplicate_num = 0
        input_path = os.path.join(input_dir, file)
        data = pandas_read_csv_file(input_path)
        for each in data:
            if len(each) != 7:
                print("length is not 7", each)
                continue
            answer_index_map = {"A": 1, "B": 2, "C": 3, "D": 4}
            answer = str(each[answer_index_map[each[5]]])
            id_str = str(each[0]) + "\n" + answer
            if id_str not in exist_questions:
                exist_questions.append(id_str)
                for i, col in enumerate(each):
                    each[i] = str(col)
                curr_subject_data.append(each)
            else:
                duplicate_num += 1
                # print("duplicate", each)
        print(file, "deplicate num is", duplicate_num)
        subject_count[file] = len(curr_subject_data)
        mmlu_data[file] = curr_subject_data
    subjects = list(subject_count.keys())
    subjects = sorted(subjects)
    for sub in subjects:
        print(sub, subject_count[sub])
        output_path = os.path.join(output_dir, sub)
        # save_to_csv_with_newlines(mmlu_data[sub], output_path)
        write_2dlist_to_csv(mmlu_data[sub], output_path)


standardize_mmlu_pro_format("../data/mmlu_pro_v1", "../data/mmlu_pro_v1")

