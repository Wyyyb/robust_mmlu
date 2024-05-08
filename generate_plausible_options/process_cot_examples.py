import json
import csv
import random
import os
import re
from tqdm import tqdm
from experiments.mmlu_pro_eval.categories import subcategories
from experiments.mmlu_pro_eval.ori_mmlu_categories import ori_mmlu_subcategories
from generate_plausible_options.stemez_add_plausible_options import *


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


def load_cot_data():
    ori_cot_data = {}
    with open(ori_mmlu_cot_data_path, "r") as fi:
        lib_data = json.load(fi)
    for k, v in lib_data.items():
        ori_cot_data[k] = parse_cot_examples(v)
    return ori_cot_data


def parse_cot_examples(v):
    segs = v.split("\n\n")
    # if len(segs) != 6:
    #     print("len(segs)", len(segs))
    ins = segs[0]
    # res = [ins]
    res = []
    for i in range(1, len(segs)):
        ori_str = segs[i]
        lines = ori_str.split("\n")
        pattern = r'\(A\) .*? \(B\) .*? \(C\) .*? \(D\) .*'
        option_line = -1
        for j, line in enumerate(lines):
            if re.search(pattern, line):
                option_line = j
                break
        if option_line == -1:
            print("option line not found. skip it.")
            for line in lines:
                print("line: ", line)
            continue
        question = "\n".join(lines[:option_line]).replace("Q: ", "")
        options_str = lines[option_line]
        answer_str = "\n".join(lines[option_line + 1:])
        pattern = r'\([ABCD]\) (.*?)(?=\([ABCD]\)|$)'
        options = re.findall(pattern, options_str)
        options = [option.strip() for option in options]
        if len(options) != 4:
            print("options length", len(options))
            print("options_str: ", options_str)
            continue
        pattern = r'The answer is \(([A-Z])\)'
        match = re.search(pattern, answer_str)
        if match:
            answer_index = "ABCD".index(match.group(1))
        else:
            print("answer_str: ", answer_str, options_str)
            print("mismatch")
            continue
        answer_content = options[answer_index]
        curr = {"question": question, "options": options, "answer": answer_content,
                "answer_symbol": match.group(1), "cot_content": answer_str}
        res.append(curr)
    return res


def save_cot_data(cot_data, output_path):
    if "ori_mmlu" in output_path:
        options_num = 4
    else:
        options_num = 10
    data = []
    for k, value in cot_data.items():
        for v in value:
            options = v["options"]
            while len(options) < options_num:
                options.append("")
            curr = [k, v["question"]] + options + [v["answer_symbol"], v["answer"], v["cot_content"]]
            if "ori_key" in v:
                curr = [v["ori_key"]] + curr
            else:
                curr = [k] + curr
            data.append(curr)
    write_2dlist_to_csv(data, output_path)


def add_plausible_options(ori_cot_data, output_path):
    if os.path.exists(output_path):
        with open(output_path, "r") as fi:
            res_cot_data = json.load(fi)
    else:
        res_cot_data = {}
    for k, value in tqdm(ori_cot_data.items()):
        new_k = subcategories.get(ori_mmlu_subcategories.get(k, ""), "")
        if new_k not in res_cot_data:
            res_cot_data[new_k] = []
        for v in value:
            question = v["question"]
            if new_k in res_cot_data:
                exist = -1
                for i, each in enumerate(res_cot_data[new_k]):
                    if each["question"] == question:
                        res_cot_data[new_k][i]["ori_key"] = k
                        exist = 1
                        break
                if exist == 1:
                    print("already exist, skip it!")
                    continue
            v["ori_key"] = k
            options = v["options"]
            answer = v["answer"]
            answer_symbol = v["answer_symbol"]
            question_str = question
            options_str = "A: {}\nB: {}\nC: {}\nD: {}".format(options[0], options[1], options[2], options[3])
            answer_str = "{}. {}".format(answer_symbol, answer)
            response = request_gpt4(question_str, options_str, answer_str,
                                    "generate_plausible_options/ins.txt")
            expanded_options = parse_options(response)
            if not expanded_options:
                print("not enough")
                continue
            new_options = options + expanded_options
            random.shuffle(new_options)
            new_ans_symbol = index_map[new_options.index(answer)]
            v["options"] = new_options
            v["answer_symbol"] = new_ans_symbol
            res_cot_data[new_k].append(v)
            with open(output_path, "w") as fo:
                fo.write(json.dumps(res_cot_data))
    with open(output_path, "w") as fo:
        fo.write(json.dumps(res_cot_data))
    return res_cot_data


def process():
    ori_cot_data = load_cot_data()
    save_cot_data(ori_cot_data, "experiments/mmlu_pro_eval/cot_lib_prompt/ori_mmlu-cot.csv")
    res_cot_data = add_plausible_options(ori_cot_data,
                                         "experiments/mmlu_pro_eval/cot_lib_prompt/res_cot_data.json")
    save_cot_data(res_cot_data, "experiments/mmlu_pro_eval/cot_lib_prompt/mmlu_pro-cot.csv")


if __name__ == '__main__':
    ori_mmlu_subcategories = {
        "abstract_algebra": "math",
        "anatomy": "health",
        "astronomy": "physics",
        "business_ethics": "business",
        "clinical_knowledge": "health",
        "college_biology": "biology",
        "college_chemistry": "chemistry",
        "college_computer_science": "computer science",
        "college_mathematics": "math",
        "college_medicine": "health",
        "college_physics": "physics",
        "computer_security": "computer science",
        "conceptual_physics": "physics",
        "econometrics": "economics",
        "electrical_engineering": "engineering",
        "elementary_mathematics": "math",
        "formal_logic": "philosophy",
        "global_facts": "other",
        "high_school_biology": "biology",
        "high_school_chemistry": "chemistry",
        "high_school_computer_science": "computer science",
        "high_school_european_history": "history",
        "high_school_geography": "geography",
        "high_school_government_and_politics": "politics",
        "high_school_macroeconomics": "economics",
        "high_school_mathematics": "math",
        "high_school_microeconomics": "economics",
        "high_school_physics": "physics",
        "high_school_psychology": "psychology",
        "high_school_statistics": "math",
        "high_school_us_history": "history",
        "high_school_world_history": "history",
        "human_aging": "health",
        "human_sexuality": "culture",
        "international_law": "law",
        "jurisprudence": "law",
        "logical_fallacies": "philosophy",
        "machine_learning": "computer science",
        "management": "business",
        "marketing": "business",
        "medical_genetics": "health",
        "miscellaneous": "other",
        "moral_disputes": "philosophy",
        "moral_scenarios": "philosophy",
        "nutrition": "health",
        "philosophy": "philosophy",
        "prehistory": "history",
        "professional_accounting": "other",
        "professional_law": "law",
        "professional_medicine": "health",
        "professional_psychology": "psychology",
        "public_relations": "politics",
        "security_studies": "politics",
        "sociology": "culture",
        "us_foreign_policy": "politics",
        "virology": "health",
        "world_religions": "philosophy"
    }
    subcategories = {
        "biology": "biology",
        "business": "business",
        "chemistry": "chemistry",
        "computer science": "computer science",
        "culture": "other",
        "economics": "economics",
        "engineering": "engineering",
        "geography": "other",
        "health": "health",
        "history": "history",
        "law": "law",
        "math": "math",
        "other": "other",
        "philosophy": "philosophy",
        "physics": "physics",
        "politics": "other",
        "psychology": "psychology"
    }
    ori_mmlu_cot_data_path = "data/cot_lib_prompt/mmlu-cot_0507.json"
    process()

