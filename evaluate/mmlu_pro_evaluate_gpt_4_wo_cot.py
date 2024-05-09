import os
from openai import AzureOpenAI
import json
import re
import random
from tqdm import tqdm
import time

API_KEY = '786f8c1ff30a4c4b9f9b8917f2f5191b'

my_client = AzureOpenAI(
  azure_endpoint="https://waterloo-gpt4.openai.azure.com/",
  api_key=API_KEY,
  api_version="2024-02-15-preview"
)


def call_gpt_4(client, instruction, inputs):
    start = time.time()
    message_text = [{"role": "user", "content": instruction + inputs}]
    completion = client.chat.completions.create(
      model="gpt-4",
      messages=message_text,
      temperature=0.7,
      max_tokens=4000,
      top_p=0.95,
      frequency_penalty=0,
      presence_penalty=0,
      stop=None
    )
    print("cost time", time.time() - start)
    return completion.choices[0].message.content


def format_example(question, options, answer):
    example = "Question: {}\nOptions: ".format(question)
    choice_map = "ABCDEFGHIJ"
    for i, opt in enumerate(options):
        example += "{}. {}\n".format(choice_map[i], opt)
    example += "Answer: " + answer
    return example


def extract_answer_wo_cot(text):
    if text.strip()[0] in ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"]:
        return text.strip()[0]
    pattern = r"answer is \(?([ABCDEFGHIJ])\)?"
    match = re.search(pattern, text)
    if match:
        return match.group(1)
    else:
        print("extraction failed:\n", text)
        return None


def single_request_gpt4(single_question, exist_result):
    global dev_examples_map
    q_id = single_question["question_id"]
    for each in exist_result:
        if q_id == each["question_id"]:
            print("already exists, skip it")
            return None, None
    category = single_question["category"]
    dev_examples = dev_examples_map[category]
    question = single_question["question"]
    options = single_question["options"]
    prompt = "The following are multiple choice questions (with answers) about {}.\n\n" \
        .format(category)
    for each in dev_examples:
        prompt += format_example(each["question"], each["options"], each["answer"])
    input_text = format_example(question, options, "")
    try:
        start = time.time()
        response = call_gpt_4(my_client, prompt, input_text)
        print("requesting gpt 4 costs: ", time.time() - start)
    except Exception as e:
        print("error", e)
        return None, None
    pred = extract_answer_wo_cot(response)
    return pred, response


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
                        if each["pred"] == each["answer"]:
                            category_record[category]["corr"] += 1
                        else:
                            category_record[category]["wrong"] += 1
            success = True
        except Exception as e:
            print("Error", e, "sleep 2 seconds")
            time.sleep(2)
    return res, category_record


def evaluate(data_dir):
    res = []
    output_res_path = os.path.join(output_dir, "eval_result_gpt_4_0509_wo_cot.json")
    output_summary_path = os.path.join(output_dir, "eval_summary_gpt_4_0509_wo_cot.json")
    category_record = {}
    res, category_record = update_result(output_res_path)
    for file in os.listdir(data_dir):
        if not file.endswith("_test.json"):
            continue
        category = file.replace("_test.json", "")
        if category not in assigned_subject:
            continue
        with open(os.path.join(data_dir, file), "r") as fi:
            data = json.load(fi)
            for each in tqdm(data):
                label = each["answer"]
                pred, response = single_request_gpt4(each, res)
                if pred is not None:
                    res, category_record = update_result(output_res_path)
                    if category not in category_record:
                        category_record[category] = {"corr": 0.0, "wrong": 0.0}
                    each["pred"] = pred
                    each["gpt_4_response"] = response
                    res.append(each)
                    if pred == label:
                        category_record[category]["corr"] += 1
                    else:
                        category_record[category]["wrong"] += 1
                    save_res(res, output_res_path)
                    save_summary(category_record, output_summary_path)
                    res, category_record = update_result(output_res_path)


def save_res(res, output_res_path):
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


def load_dev_examples(input_dir):
    global dev_examples_map
    for file in os.listdir(input_dir):
        if not file.endswith("_dev.json"):
            continue
        with open(os.path.join(input_dir, file), 'r') as fi:
            curr = json.load(fi)
            dev_examples_map[file.replace("_dev.json", "")] = curr


if __name__ == '__main__':
    assigned_subject = ["biology", "business", "chemistry", "computer science", "history"]
    output_dir = "../experiments/eval_result_0509_gpt_4/"
    dev_dir = "../data/mmlu_pro_v1_0509/dev"
    test_dir = "../data/mmlu_pro_v1_0509/test"
    os.makedirs(output_dir, exist_ok=True)
    dev_examples_map = {}
    load_dev_examples(dev_dir)
    evaluate(test_dir)

