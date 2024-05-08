import json
import os
import csv
import random

global_sta = {}
lead_time_sta = {}


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


def postprocess(input_file, output_dir, sample=""):
    os.makedirs(output_dir, exist_ok=True)
    res_data = {}
    q_id = 0
    save_by_tags = {}
    global lead_time_sta
    with open(input_file, "r") as fi:
        data = json.load(fi)
    four_options_data = load_4_options_questions()
    for each in data:
        annotator_id = each["annotator"]
        annotator = match_annotator(annotator_id)
        if annotator not in lead_time_sta:
            lead_time_sta[annotator] = 0
        lead_time = each.get("lead_time", 0)
        if lead_time > 600:
            lead_time = 600
        lead_time_sta[annotator] += lead_time / 3600
        question = each["meta_info"]["question"]
        # options = each["meta_info"]["options"]
        options, answer, tag = process_options(each, four_options_data)
        if tag == "invalid":
            print("ref id is", each["ref_id"])
        if tag != "no_issues":
            if tag not in save_by_tags:
                save_by_tags[tag] = []
            save_by_tags[tag].append(each)
        if not options:
            continue
        answer_index = "ABCDEFGHIJKLMNOPQRSTUVWXYZ".index(answer)
        src = each["meta_info"]["src"]
        subject = each["meta_info"]["subject"]
        if subject not in res_data:
            res_data[subject] = []
        curr = {"q_id": q_id, "question": question, "options": options, "answer": answer,
                "answer_index": answer_index, "src": src}
        res_data[subject].append(curr)
        q_id += 1
    save_ann_tag_data(save_by_tags, "ann_tag_data/")
    save_res_data(res_data, output_dir, sample)
    save_global_sta()


def save_global_sta():
    with open("annotator_sta_0505.json", "w") as fo:
        fo.write(json.dumps(global_sta))
    with open("lead_time_sta_0505.json", "w") as fo:
        fo.write(json.dumps(lead_time_sta))
    summary_sta = {}
    no_issues_count = 0
    for annotator, v in global_sta.items():
        no_issues_count += v.get("no_issues", 0)
        for key, value in v.items():
            if key not in summary_sta:
                summary_sta[key] = 0
            summary_sta[key] += value
    with open("summary_sta_0505.json", "w") as fo:
        fo.write(json.dumps(summary_sta))


def save_res_data(res_data, output_dir, sample=""):
    other_cat = ["culture.csv", "geography.csv", "politics.csv", "other.csv"]
    keys = list(res_data.keys())
    keys = sorted(keys)
    other_data = []
    for k in keys:
        v = res_data[k]
        if k in other_cat:
            other_data += v
            continue
        random.shuffle(v)
        output_path = os.path.join(output_dir, k.replace(".csv", ".json"))
        with open(output_path, "w") as fo:
            if sample == "sample":
                v = v[:10]
            fo.write(json.dumps(v))
            print("number of", k, len(v))
    random.shuffle(other_data)
    output_path = os.path.join(output_dir, "other.json")
    with open(output_path, "w") as fo:
        if sample == "sample":
            other_data = other_data[:10]
        fo.write(json.dumps(other_data))
        print("number of other", len(other_data))


def save_ann_tag_data(save_by_tags, output_dir):
    for k, v in save_by_tags.items():
        output_path = os.path.join(output_dir, k + ".json")
        with open(output_path, "w") as fo:
            fo.write(json.dumps(v))
            print("number of", k, len(v))


def load_4_options_questions(input_dir=""):
    res = {}
    if input_dir == "":
        input_dir = "../experiments/data/mmlu_pro_4_options"
    for file in os.listdir(input_dir):
        file_path = os.path.join(input_dir, file)
        curr = read_csv_file(file_path)
        for each in curr:
            question = each[0]
            options = each[1: 5]
            answer = each[5]
            answer_index = "ABCD".index(answer)
            answer_content = options[answer_index]
            question_id = question + "\n" + answer_content
            if question_id not in res:
                res[question_id] = [question] + options + [answer]
    return res


def recall_4_options_questions(four_options_data, ann):
    index_map_str = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    answer = ann["meta_info"]["answer"]
    options = ann["meta_info"]["options"]
    question = ann["meta_info"]["question"]
    answer_index = index_map_str.index(answer)
    answer_content = options[answer_index]
    question_id = question + "\n" + answer_content
    if question_id not in four_options_data:
        return None, None
    temp = four_options_data[question_id]
    options_new = temp[1: 5]
    answer_new = temp[5]
    return options_new, answer_new


def process_options(ann, four_options_data):
    global global_sta
    annotator = match_annotator(ann["annotator"])
    if annotator not in global_sta:
        global_sta[annotator] = {}
    index_map_str = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    answer = ann["meta_info"]["answer"]
    options = ann["meta_info"]["options"]
    answer_index = index_map_str.index(answer)
    answer_content = options[answer_index]

    if "meta_options_issue" in ann:
        if "meta_options_issue" not in global_sta[annotator]:
            global_sta[annotator]["meta_options_issue"] = 1
        else:
            global_sta[annotator]["meta_options_issue"] += 1
        return None, None, "meta_options_issue"
    if "hard_to_verify" in ann:
        if "hard_to_verify" not in global_sta[annotator]:
            global_sta[annotator]["hard_to_verify"] = 1
        else:
            global_sta[annotator]["hard_to_verify"] += 1
        options, answer = recall_4_options_questions(four_options_data, ann)
        return options, answer, "hard_to_verify"
    if "transcription" in ann and "irrelevant_options" not in ann:
        if "question_unsure" not in global_sta[annotator]:
            global_sta[annotator]["question_unsure"] = 1
        else:
            global_sta[annotator]["question_unsure"] += 1
        options, answer = recall_4_options_questions(four_options_data, ann)
        return options, answer, "question_unsure"
    if "bad_questions" in ann:
        if "bad_questions" not in global_sta[annotator]:
            global_sta[annotator]["bad_questions"] = 1
        else:
            global_sta[annotator]["bad_questions"] += 1
        return None, None, "bad_questions"

    if "irrelevant_options" in ann:
        if "unsure_options" not in global_sta[annotator]:
            global_sta[annotator]["unsure_options"] = 1
        else:
            global_sta[annotator]["unsure_options"] += 1

        if isinstance(ann["irrelevant_options"], str):
            duplicate_correct_answers = [ann["irrelevant_options"]]
        elif isinstance(ann["irrelevant_options"], dict):
            duplicate_correct_answers = ann["irrelevant_options"]["choices"]
        else:
            print("unsure_options format error", ann["irrelevant_options"])
            duplicate_correct_answers = []
        rm_option_index = []
        res_options = []
        for each in duplicate_correct_answers:
            option = each.replace("Option ", "")
            opt_index = index_map_str.index(option)
            rm_option_index.append(opt_index)
        for i, option in enumerate(options):
            if i in rm_option_index and option != answer_content:
                continue
            res_options.append(option)
        answer = index_map_str[res_options.index(answer_content)]
        return res_options, answer, "unsure_options"

    if "duplicate_correct_answer" in ann:
        if "duplicate_correct_answer" not in global_sta[annotator]:
            global_sta[annotator]["duplicate_correct_answer"] = 1
        else:
            global_sta[annotator]["duplicate_correct_answer"] += 1

        if isinstance(ann["duplicate_correct_answer"], str):
            duplicate_correct_answers = [ann["duplicate_correct_answer"]]
        elif isinstance(ann["duplicate_correct_answer"], dict):
            duplicate_correct_answers = ann["duplicate_correct_answer"]["choices"]
        else:
            print("duplicate_correct_answers format error", ann["duplicate_correct_answer"])
            duplicate_correct_answers = []
        rm_option_index = []
        res_options = []
        for each in duplicate_correct_answers:
            option = each.replace("Option ", "")
            opt_index = index_map_str.index(option)
            rm_option_index.append(opt_index)
        for i, option in enumerate(options):
            if i in rm_option_index and option != answer_content:
                continue
            res_options.append(option)
        answer = index_map_str[res_options.index(answer_content)]
        return res_options, answer, "duplicate_correct_answer"
    if "answer_is_incorrect" in ann:
        if "answer_is_incorrect" not in global_sta[annotator]:
            global_sta[annotator]["answer_is_incorrect"] = 1
        else:
            global_sta[annotator]["answer_is_incorrect"] += 1
        return None, None, "answer_is_incorrect"
    if "no_issues" not in global_sta[annotator]:
        global_sta[annotator]["no_issues"] = 1
    else:
        global_sta[annotator]["no_issues"] += 1
    if "no_issues" in ann:
        return options, answer, "no_issues"
    return None, None, "invalid"


def match_annotator(annntator_id):
    annotator_map = {8: "kai wang", 9: "a2arulra", 10: "tianle li", 11: "Yuansheng Ni",
                     12: "max ku", 13: "weiming ren", 15: "ziyan jiang",
                     16: "Abhranil Chandra", 17: "shiguang guo", 18: "xuan he",
                     19: "alex zhuang", 21: "gezhang", 22: "richard fan"}
    return annotator_map.get(annntator_id, "")


if __name__ == '__main__':
    # postprocess("data/ann_data_0505.json", "../data/mmlu_pro_v1_0506")
    postprocess("data/ann_data_0505.json", "../data/mmlu_pro_v1_sample", "sample")

