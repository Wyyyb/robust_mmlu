import json
import re
import os


def collect():
    include_ans_data = []
    exclude_ans_data = []
    count = 0
    law_count = 0
    wrong_count = 0
    input_path = "data/model_outputs_pro_5shots_16_51_04.json"
    with open(input_path, "r") as fi:
        info = json.load(fi)
    for each in info:
        content = each["rationale"]
        answer = each["answer"]
        pred = extract_answer(content)
        if answer not in pred:
            wrong_count += 1
        each["gemini_pred"] = pred
        if len(pred) >= 2:
            if answer in pred:
                include_ans_data.append(each)
            else:
                exclude_ans_data.append(each)
            if each["category"] == "law":
                law_count += 1
            count += 1
    print(count)
    print(law_count)
    print(wrong_count)
    # format_data(include_ans_data, "include_ans_data", 100)
    # format_data(exclude_ans_data, "exclude_ans_data", 100)


def format_data(input_data, output_dir, single_num=200):
    res = []
    for each in input_data:
        symbol_str = "ABCDEFGHIJ"
        options_str = ""
        options = each["options"]
        temp = []
        for opt in options:
            if opt != "N/A":
                temp.append(opt)
        options = temp
        answer = each["answer"]
        question = each["question"]
        q_id = each["question_id"]
        subject = each["category"]
        rationale = each["rationale"]
        src = each["src"]
        for i in range(len(options)):
            options_str += symbol_str[i] + ". " + options[i] + "\n"
        text = f"Question:\n{question}\n\nOptions:\n{options_str}\nAnswer: {answer}\n\n" \
               f"Gemini Rational:\n{rationale}"
        meta_info = {"subject": subject, "src": src, "question": question, "options": options,
                     "answer": answer, "rational": rationale, "gemini_pred": each["gemini_pred"]}
        curr_res = {"text": text, "ref_id": q_id, "meta_info": meta_info}
        res.append(curr_res)
    transfer_to_label_studio(res, output_dir, single_num)


def transfer_to_label_studio(res, output_dir, single_num):
    os.makedirs(output_dir, exist_ok=True)
    i = 0
    while i < len(res):
        if i + single_num < len(res):
            end_index = i + single_num
        else:
            end_index = len(res)
        with open(output_dir + f"/part_{i//single_num}.json", "w") as fo:
            fo.write(json.dumps(res[i: end_index]))
        i = end_index


def extract_answer(content):
    ori_content = content
    sentence = ""
    while "nswer is" in content:
        start_index = content.index("nswer is") + len("nswer is")
        content = content[: content.index("nswer is")] + "*"*len("nswer is") + content[start_index:]
        sentence = content[start_index:].split("\n")[0]

    # 定义正则表达式，匹配非单词边界后面跟着 A 到 J 的单个字符，并且这些字符前后不能有其他字母或数字
    pattern = r'(?<!\w)[A-J](?!\w)'

    # 使用 findall 方法查找所有匹配的字符
    matches = re.findall(pattern, sentence)
    return matches


if __name__ == '__main__':
    collect()



