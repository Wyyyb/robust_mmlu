import csv
import json
import os


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


def transfer(input_dir, output_dir, sample_dir=""):
    os.makedirs(output_dir, exist_ok=True)
    if sample_dir != "":
        os.makedirs(sample_dir, exist_ok=True)
    exist_questions = []
    file_list = list(os.listdir(input_dir))
    file_list = sorted(file_list)
    q_id = 0
    for each in file_list:
        if not each.endswith(".csv"):
            continue
        res = []
        file_path = os.path.join(input_dir, each)
        data = read_csv_file(file_path)
        width = len(data[0])
        option_num = width - 3
        for row in data:
            question_str = row[0]
            options = row[1: option_num + 1]
            answer = row[-2]
            answer_index = "ABCDEFGHIJKLMNOPQRSTUVWXYZ".index(answer)
            src = row[-1]
            question_id = question_str + "\n" + options[answer_index]
            if question_id in exist_questions:
                continue
            curr_res = {"q_id": q_id, "question": question_str, "options": options, "answer": answer,
                        "answer_index": answer_index, "src": src}
            q_id += 1
            res.append(curr_res)
        output_path = os.path.join(output_dir, each.replace(".csv", ".json").replace("_test", ""))
        sample_path = os.path.join(sample_dir, each.replace(".csv", ".json").replace("_test", ""))
        with open(output_path, "w") as fo:
            fo.write(json.dumps(res))
        print(each, "question number is: ", len(res))
        if sample_dir != "":
            with open(sample_path, "w") as fo:
                fo.write(json.dumps(res[:10]))


if __name__ == "__main__":
    # transfer("experiments/data/mmlu_pro_exp_10_options", "data/mmlu_pro_exp_10_options")
    transfer("experiments/data/ori_mmlu_data", "data/ori_mmlu_data_json",
             "data/ori_mmlu_sample")







