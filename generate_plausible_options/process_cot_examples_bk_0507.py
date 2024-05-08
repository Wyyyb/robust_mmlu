import json
import random
import os
import re
from experiments.mmlu_pro_eval.categories import subcategories
from experiments.mmlu_pro_eval.ori_mmlu_categories import ori_mmlu_subcategories
from generate_plausible_options.stemez_add_plausible_options import *


def load_mmlu_pro(input_dir):
    res = {}
    for file in os.listdir(input_dir):
        file_path = os.path.join(input_dir, file)
        with open(file_path, 'r') as fi:
            curr = json.load(fi)
            for each in curr:
                question = each["question"]
                answer_content = each["options"][each["answer_index"]]
                if question + "\n" + answer_content not in res:
                    res[question + "\n" + answer_content] = each
    return res


def single_process(mmlu_pro_data, k, v):
    prompt = "The following are multiple choice questions (with answers) about {}\n\n".format(k)
    temp = []
    for each in v:
        lines = each.split("\n")
        pattern = r'\(A\) [^()]+ \(B\) [^()]+ \(C\) [^()]+ \(D\) [^()]+'
        option_line = -1
        for i, line in enumerate(lines):
            if re.search(pattern, line):
                option_line = i
                break
        if option_line == -1:
            return None
        question = "\n".join(lines[:option_line]).replace("Q: ", "")
        options_str = lines[option_line]
        answer_str = "\n".join(lines[option_line + 1:])
        pattern = r'\([A-Z]\) [^()]+'
        options = re.findall(pattern, options_str)
        options = [option.strip()[4:] for option in options]
        pattern = r'The answer is \(([A-Z])\)'
        match = re.search(pattern, answer_str)
        if match:
            answer_index = "ABCD".index(match.group(1))
        else:
            answer_index = -1
            print("mismatch")
        answer_content = options[answer_index]
        question_id = question + "\n" + answer_content
        if question_id not in mmlu_pro_data:
            print("not found in mmlu pro data")
            print(k, question_id)
            curr = [options, each]
            temp.append(curr)
            continue
        mmlu_pro_curr = mmlu_pro_data[question_id]
        options = mmlu_pro_curr["options"]
        answer_content = options[mmlu_pro_curr["answer_index"]]
        random.shuffle(options)
        new_answer_index = options.index(answer_content)
        combo = f"Q: {question}\n"
        index_map = "ABCDEFGHIJ"
        for i, opt in enumerate(options):
            combo += f"({index_map[i]}) {opt} "
        combo = combo[:-1] + "\n"
        combo += answer_str
        combo = combo[:-3] + index_map[new_answer_index] + ")."
        curr = [options, combo]
        temp.append(curr)
    temp = sorted(temp, key=lambda x: -len(x[0]))
    for i in range(5):
        prompt += temp[i][1] + "\n\n"
    return


def process():
    mmlu_pro_data = load_mmlu_pro("data/mmlu_pro_v1_0506")
    with open("data/cot_lib_prompt/mmlu-cot.json", "r") as fi:
        lib_data = json.load(fi)
    ori_cat = ori_mmlu_subcategories
    pro_cat = subcategories
    cot_lib = {}
    for k, v in lib_data.items():
        key = pro_cat.get(ori_cat.get(k, ""), "")
        if key not in cot_lib:
            cot_lib[key] = []
        cot_lib[key] += v.split("\n\n")[1:]
    for k, v in cot_lib.items():
        res = single_process(mmlu_pro_data, k, v)
        cot_lib[k] = res
    with open("experiments/mmlu_pro_eval/cot_lib_prompt/mmlu_pro-cot.json", "w") as fo:
        fo.write(json.dumps(cot_lib))


if __name__ == '__main__':
    process()

