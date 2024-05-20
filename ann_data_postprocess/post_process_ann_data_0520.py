import os
import json


def postprocess(input_files, output_file):
    res_data = {}
    save_by_tags = {}
    data = []
    for input_file in input_files:
        with open(input_file, "r") as fi:
            data += json.load(fi)
    for each in data:
        question = each["meta_info"]["question"]
        bad_question = False
        q_id = each["ref_id"]
        # options = each["meta_info"]["options"]
        options, answer, tag = process_options(each)
        if tag == "invalid":
            print("invalid, ref id is", each["ref_id"])
        if tag != "no_issues":
            if tag not in save_by_tags:
                save_by_tags[tag] = []
            save_by_tags[tag].append(each)
        else:
            continue
        if not options:
            bad_question = True
            answer_index = -1
        else:
            answer_index = "ABCDEFGHIJKLMNOPQRSTUVWXYZ".index(answer)
        src = each["meta_info"]["src"]
        subject = each["meta_info"]["subject"]
        if subject not in res_data:
            res_data[subject] = []
        curr = {"question_id": q_id, "question": question, "options": options, "answer": answer,
                "answer_index": answer_index, "src": src, "category": subject, "bad_question": bad_question}
        res_data[subject].append(curr)
    print("rm_options_sta", rm_options_sta)
    save(res_data, output_file)


def save(res_data, output_file):
    sta = {}
    res = []
    for k, v in res_data.items():
        if k not in sta:
            sta[k] = 0
        sta[k] += len(v)
        res += v
    print("total num is: ", len(res))
    print("sta", sta)
    with open(output_file, "w") as fo:
        fo.write(json.dumps(res))


def process_options(ann):
    index_map_str = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    answer = ann["meta_info"]["answer"]
    options = ann["meta_info"]["options"]
    answer_index = index_map_str.index(answer)
    answer_content = options[answer_index]

    if "meta_options_issue" in ann:
        return None, None, "meta_options_issue"
    if "hard_to_verify" in ann:
        return None, None, "hard_to_verify"
    if "transcription" in ann and "irrelevant_options" not in ann:
        return None, None, "hard_to_verify"
    if "bad_questions" in ann:
        return None, None, "bad_questions"
    if "answer_is_incorrect" in ann:
        return None, None, "answer_is_incorrect"

    if "unsure_options" in ann or "duplicate_correct_answer" in ann:
        duplicate_correct_answers_1, duplicate_correct_answers_2 = [], []
        if "unsure_options" in ann:
            if isinstance(ann["unsure_options"], str):
                duplicate_correct_answers_1 = [ann["unsure_options"]]
            elif isinstance(ann["unsure_options"], dict):
                duplicate_correct_answers_1 = ann["unsure_options"]["choices"]
            else:
                print("unsure_options format error", ann["unsure_options"])
                duplicate_correct_answers_1 = []
        if "duplicate_correct_answer" in ann:
            if isinstance(ann["duplicate_correct_answer"], str):
                duplicate_correct_answers_2 = [ann["duplicate_correct_answer"]]
            elif isinstance(ann["duplicate_correct_answer"], dict):
                duplicate_correct_answers_2 = ann["duplicate_correct_answer"]["choices"]
            else:
                print("duplicate_correct_answers format error", ann["duplicate_correct_answer"])
                duplicate_correct_answers_2 = []
        duplicate_correct_answers = duplicate_correct_answers_1 + duplicate_correct_answers_2
        rm_option_index = []
        res_options = []
        for each in duplicate_correct_answers:
            option = each.replace("Option ", "")
            opt_index = index_map_str.index(option)
            rm_option_index.append(opt_index)
        for i, option in enumerate(options):
            if i in rm_option_index and option != answer_content:
                if ann["meta_info"]["subject"] not in rm_options_sta:
                    rm_options_sta[ann["meta_info"]["subject"]] = 0
                rm_options_sta[ann["meta_info"]["subject"]] += 1
                continue
            res_options.append(option)
        answer = index_map_str[res_options.index(answer_content)]
        return res_options, answer, "duplicate_correct_options"

    if "no_issues" in ann:
        return options, answer, "no_issues"
    return None, None, "invalid"


if __name__ == "__main__":
    rm_options_sta = {}
    postprocess(["ann_data/ann_data_part_1_0520.json", "ann_data/ann_data_part_2_0520.json"],
                "data/ann_modified_data_0520.json")

