import csv
import os
import json
import re
import random


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


def merge_result(dir_path):
    res = []
    for file in os.listdir(dir_path):
        if not file.endswith("result.json"):
            continue
        file_path = os.path.join(dir_path, file)
        with open(file_path, "r") as fi:
            curr = json.load(fi)
        res += curr
    # with open(output_path, "w") as fo:
    #     fo.write(json.dumps(res, indent=2))
    return res


def extract_answer(text):
    pattern = r"answer is \(?([A-J])\)?"
    match = re.search(pattern, text)
    if match:
        return match.group(1)
    else:
        print("1st answer extract failed\n" + text)
        return extract_again(text)


def extract_again(text):
    match = re.search(r'.*[aA]nswer:\s*([A-J])', text)
    if match:
        return match.group(1)
    else:
        return extract_final(text)


def extract_final(text):
    pattern = r"\b[A-J]\b(?!.*\b[A-J]\b)"
    match = re.search(pattern, text, re.DOTALL)
    if match:
        return match.group(0)
    else:
        return None


def post_process_single(ori_result, output_path, sta_path, model_name=None):
    if os.path.exists(sta_path):
        sta_csv_data = read_csv_file(sta_path)
    else:
        sta_csv_data = []
    if not model_name:
        model_name = output_path.split("_")[2]
    merged_res = ori_result
    sta_map = {}
    csv_header = ["Models", "Overall", "Biology", "Business", "Chemistry", "Computer Science",
                  "Economics", "Engineering", "Health", "History", "Law", "Math", "Philosophy",
                  "Physics", "Psychology", "Other"]
    res = []
    for each in merged_res:
        cat = each["category"]
        if cat not in sta_map:
            sta_map[cat] = {"corr": 0.0, "wrong": 0.0}
        if "generated_text" in each:
            pred = extract_answer(each["generated_text"])
            if pred is None:
                random.seed(12345)
                pred = random.choice(["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"])
        elif "model_outputs" in each:
            pred = extract_answer(each["model_outputs"])
            if pred is None:
                random.seed(12345)
                pred = random.choice(["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"])
            # if pred != each["pred"]:
            #     print("inconsistent pred", each, pred)
        else:
            pred = each["pred"]
        each["pred"] = pred
        res.append(each)
        if pred == each["answer"]:
            sta_map[cat]["corr"] += 1
        else:
            sta_map[cat]["wrong"] += 1
    total_corr = 0.0
    total_wrong = 0.0
    for k, v in sta_map.items():
        total = v["corr"] + v["wrong"] + 0.0001
        accu = round(v["corr"] / total, 4)
        sta_map[k]["accu"] = accu
        total_corr += v["corr"]
        total_wrong += v["wrong"]
    total_accu = round(total_corr / (total_corr + total_wrong + 0.0001), 4)
    curr = [model_name, total_accu]
    for i, item in enumerate(csv_header):
        if i <= 1:
            continue
        cat = item.lower()
        if cat not in sta_map:
            print("cat not in sta_map", cat)
            continue
        curr.append(sta_map[cat]["accu"])
    sta_csv_data.append(curr)
    write_2dlist_to_csv(sta_csv_data, sta_path)
    with open(output_path, "w") as fo:
        fo.write(json.dumps(res, indent=2))


def run_single(input_path, output_path, sta_path, model_name=None):
    if ".json" in input_path:
        with open(input_path, "r") as fi:
            ori_res = json.load(fi)
    else:
        ori_res = merge_result(input_path)
    post_process_single(ori_res, output_path, sta_path, model_name)


if __name__ == "__main__":
    # run_single("../eval_results/model_outputs_Meta-Llama-3-8B_5shots.json",
    #            "./model_outputs_Meta-Llama-3-8B_5shots_0711.json",
    #            "./submission.csv",
    #            "meta-llama/Meta-Llama-3-8B")
    run_single("eval_results_0719/mathstral-7B-v0.1",
               "eval_results_0719/mathstral-7B-v0.1/model_outputs_mathstral-7B_5shots.json",
               "./submission.csv",
               "Mathstral-7B-v0.1")




