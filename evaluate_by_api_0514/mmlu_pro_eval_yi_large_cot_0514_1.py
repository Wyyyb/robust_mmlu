import os
from openai import AzureOpenAI
import json
import re
import random
from tqdm import tqdm
import time
from openai import OpenAI

API_BASE = "https://api.lingyiwanwu.com/v1"
API_KEY = "ef798a2b5d834a1b8d6f2e69d83b22c7"


my_client = OpenAI(
    # defaults to os.environ.get("OPENAI_API_KEY")
    api_key=API_KEY,
    base_url=API_BASE
)


def call_gpt_4(client, instruction, inputs):
    start = time.time()
    message_text = [{"role": "user", "content": instruction + inputs}]
    completion = client.chat.completions.create(
        model="yi-large",
        messages=message_text,
        temperature=0,
        max_tokens=4000,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
        stop=None
    )
    print("cost time", time.time() - start)
    res = completion.choices[0].message.content
    return res


def format_example(question, options, cot_content=""):
    if cot_content == "":
        cot_content = "Let think step by step."
    if cot_content.startswith("A: "):
        cot_content = cot_content[3:]
    example = "Question: {}\nOptions: ".format(question)
    choice_map = "ABCDEFGHIJ"
    for i, opt in enumerate(options):
        example += "{}. {}\n".format(choice_map[i], opt)
    if cot_content == "":
        example += "Answer: "
    else:
        example += "Answer: " + cot_content + "\n\n"
    return example


def extract_answer(text):
    pattern = r"answer is \(?([ABCDEFGHIJ])\)?"
    match = re.search(pattern, text)
    if match:
        return match.group(1)
    else:
        print("extraction failed:\n", text)
        return None


def single_request_gpt4(single_question, exist_result):
    global cot_examples_map
    exist = True
    q_id = single_question["question_id"]
    for each in exist_result:
        if q_id == each["question_id"] and single_question["question"] == each["question"]:
            print("already exists, skip it")
            return each["pred"], each["gpt_4_response"], exist
    exist = False
    category = single_question["category"]
    cot_examples = cot_examples_map[category]
    question = single_question["question"]
    options = single_question["options"]
    prompt = "You are an expert in {}. Below is a series of example questions (with answers) " \
             "about {} for demonstration. You will be given a question at the end, after the " \
             "examples, for you to answer. First give step-by-step reasoning about how to solve " \
             "the question. Then output the answer in the format of \"The answer is (X)\" at " \
             "the end.\n\n".format(category, category)
    # prompt = "The following are multiple choice questions (with answers) about {}. Think step by" \
    #          " step and then output the answer in the format of \"The answer is (X)\" at the end.\n\n" \
    #     .format(category)
    for each in cot_examples:
        prompt += format_example(each["question"], each["options"], each["cot_content"])
    input_text = format_example(question, options)
    try:
        start = time.time()
        response = call_gpt_4(my_client, prompt, input_text)
        print("requesting gpt 4 costs: ", time.time() - start)
    except Exception as e:
        print("error", e)
        return None, None, exist
    pred = extract_answer(response)
    return pred, response, exist


def update_result(output_res_path):
    category_record = {}
    res = []
    success = False
    while not success:
        try:
            if os.path.exists(output_res_path):
                with open(output_res_path, "r") as fi:
                    res = json.load(fi)
                    for each in res:
                        category = each["category"]
                        if category not in category_record:
                            category_record[category] = {"corr": 0.0, "wrong": 0.0}
                        if not each["pred"]:
                            category_record[category]["wrong"] += 1
                        elif each["pred"] == each["answer"]:
                            category_record[category]["corr"] += 1
                        else:
                            category_record[category]["wrong"] += 1
            success = True
        except Exception as e:
            print("Error", e, "sleep 2 seconds")
            time.sleep(2)
    return res, category_record


def evaluate(data_dir):
    ori_output_res_path = os.path.join(output_dir, "eval_result_gpt_4_0510.json")
    ori_output_summary_path = os.path.join(output_dir, "eval_summary_gpt_4_0510.json")
    for file in os.listdir(data_dir):
        if not file.endswith("_test.json"):
            continue
        category = file.replace("_test.json", "")
        output_res_path = ori_output_res_path.replace(".json", "_" + category.replace(" ", "_") + ".json")
        output_summary_path = ori_output_summary_path.replace(".json", "_" + category.replace(" ", "_") + ".json")
        res, category_record = update_result(output_res_path)
        if assigned_subject and category not in assigned_subject:
            continue
        with open(os.path.join(data_dir, file), "r") as fi:
            data = json.load(fi)
            for each in tqdm(data):
                label = each["answer"]
                print("category:", category)
                pred, response, exist = single_request_gpt4(each, res)
                if exist:
                    continue
                if response is not None:
                    res, category_record = update_result(output_res_path)
                    if category not in category_record:
                        category_record[category] = {"corr": 0.0, "wrong": 0.0}
                    each["pred"] = pred
                    each["gpt_4_response"] = response
                    res.append(each)
                    if pred is not None:
                        if pred == label:
                            category_record[category]["corr"] += 1
                        else:
                            category_record[category]["wrong"] += 1
                    else:
                        category_record[category]["wrong"] += 1
                    save_res(res, output_res_path)
                    save_summary(category_record, output_summary_path)
                    res, category_record = update_result(output_res_path)
            save_res(res, output_res_path)
            save_summary(category_record, output_summary_path)


def save_res(res, output_res_path):
    temp = []
    exist_q_id = []
    for each in res:
        if each["question_id"] not in exist_q_id:
            exist_q_id.append(each["question_id"])
            temp.append(each)
        else:
            continue
    res = temp
    with open(output_res_path, "w") as fo:
        fo.write(json.dumps(res))


def save_summary(category_record, output_summary_path):
    total_corr = 0.0
    total_wrong = 0.0
    for k, v in category_record.items():
        if k == "total":
            continue
        cat_acc = v["corr"] / (v["corr"] + v["wrong"])
        category_record[k]["acc"] = cat_acc
        total_corr += v["corr"]
        total_wrong += v["wrong"]
    acc = total_corr / (total_corr + total_wrong)
    category_record["total"] = {"corr": total_corr, "wrong": total_wrong, "acc": acc}
    with open(output_summary_path, "w") as fo:
        fo.write(json.dumps(category_record))


def load_cot_examples(input_dir):
    global cot_examples_map
    for file in os.listdir(input_dir):
        if not file.endswith("_dev.json"):
            continue
        with open(os.path.join(input_dir, file), 'r') as fi:
            curr = json.load(fi)
            cot_examples_map[file.replace("_dev.json", "")] = curr


if __name__ == '__main__':
    # assigned_subject = ["business", "chemistry", "computer science"]
    assigned_subject = ["economics", "engineering", "health", "physics"]
    output_dir = "../experiments/eval_result_0514_yi_large_cot/"
    dev_dir = "../data/mmlu_pro_v1_0512/dev"
    test_dir = "../data/mmlu_pro_v1_0512/test"
    os.makedirs(output_dir, exist_ok=True)
    cot_examples_map = {}
    load_cot_examples(dev_dir)
    evaluate(test_dir)

