import json
import csv
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


def sta_ann_result(ann_res):
    output_path = "sta_ann_0415.csv"
    subjects = list(ann_res.keys())
    subjects = sorted(subjects)
    res_data = [["subject", "ref_id", "question", "options", "answer", "solution", "no_issues",
                 "not_a_good_mcq", "incomplete_answer", "too_obvious_answer", "others"]]
    for subject in subjects:
        for k, v in ann_res[subject].items():
            transcript = v["transcription"]
            no_issues = 0
            not_a_good_mcq = 0
            incomplete_answer = 0
            too_obvious_answer = 0
            others = ""
            if transcript != "":
                others = transcript
            if "No issues" in v["ann_issue"]:
                no_issues = 1
            if "Not a good MCQ" in v["ann_issue"]:
                not_a_good_mcq = 1
            if "Too Obvious Answer" in v["ann_issue"]:
                too_obvious_answer = 1
            if "Incomplete Answer Extraction" in v["ann_issue"]:
                incomplete_answer = 1
            options = v["options"]
            options_str = f"A. {options[0]}\nB. {options[1]}\nC. {options[2]}\nD. {options[3]}"
            res_data.append([subject, v["ref_id"], v["question"], options_str, v["answer"],
                             v["solution"], no_issues, not_a_good_mcq, incomplete_answer,
                             too_obvious_answer, others])
    write_2dlist_to_csv(res_data, output_path)


def postprocess():
    with open(ann_data_path, "r") as fi:
        temp = json.load(fi)
    ann_data = {}
    for each in temp:
        meta_info = each["meta_info"]
        src = meta_info["src"]
        subject = meta_info["subject"]
        if "transcription" in each:
            transcription = each["transcription"]
        else:
            transcription = ""
        if "sentiment" not in each:
            ann_issue = ""
        else:
            ann_issue = each["sentiment"]
        if isinstance(ann_issue, str):
            ann_issue = [ann_issue]
        elif isinstance(ann_issue, dict):
            ann_issue = ann_issue["choices"]
        question = meta_info["question"]
        options = meta_info["options"]
        question_str = question + "\n" + "\n".join(options)
        if subject not in ann_data:
            ann_data[subject] = {}
        if question_str not in ann_data[subject]:
            ann_data[subject][question_str] = {"src": src, "ann_issue": ann_issue, "question": question,
                                               "options": options, "transcription": transcription,
                                               "ref_id": each["ref_id"], "solution": meta_info["solution"],
                                               "answer": meta_info["answer"]}
        else:
            # print("duplicate question_str", question_str, subject)
            continue
    sta_ann_result(ann_data)


if __name__ == '__main__':
    input_dir = r"../experiments/data/images_removed_mmlu"
    output_dir = r"../experiments/data/mmlu_pro_v1_1"
    ann_data_path = r"../experiments/data/ann_data_phase_1/project-at-2024-04-15.json"
    postprocess()

