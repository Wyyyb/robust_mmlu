import csv
import os
import random
import json
from openai import AzureOpenAI
from tqdm import tqdm
import re


API_KEY = '786f8c1ff30a4c4b9f9b8917f2f5191b'

my_client = AzureOpenAI(
  azure_endpoint="https://waterloo-gpt4.openai.azure.com/",
  api_key=API_KEY,
  api_version="2024-02-15-preview"
)


def call_gpt_4(client, instruction, inputs):
    message_text = [{"role": "user", "content": instruction + inputs}]
    completion = client.chat.completions.create(
      model="gpt-4",
      messages=message_text,
      temperature=0.7,
      max_tokens=2000,
      top_p=0.95,
      frequency_penalty=0,
      presence_penalty=0,
      stop=None
    )
    return completion.choices[0].message.content


def read_csv_file(file_path):
    with open(file_path, mode='r', encoding='utf-8') as file:
        csv_reader = csv.reader(file)
        data = list(csv_reader)
    return data


def write_2dlist_to_csv(data, file_name):
    with open(file_name, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerows(data)


scibench_map = {"fund": "physics.csv", "thermo": "physics.csv", "class": "physics.csv",
                "quan": "chemistry.csv", "chemmc": "chemistry.csv", "atkins": "chemistry.csv",
                "matter": "chemistry.csv", "calculus": "math.csv", "stat": "math.csv", "diff": "math.csv"}

scibench_list = ["chemistry.csv", "math.csv", "physics.csv"]


def load_ori_scibench(data_dir):
    res = []
    file_list = list(os.listdir(data_dir))
    file_list.sort(key=str.lower)
    for file in file_list:
        if file.replace(".json", "") not in scibench_map:
            continue
        with open(os.path.join(data_dir, file), "r") as fi:
            data = json.load(fi)
        data.sort(key=lambda x: x["problem_text"])
        for each in data:
            question = each["problem_text"]
            src = "scibench-" + file.replace(".json", "")
            answer = each["answer_latex"]
            if each["unit"].replace(" ", "") != "":
                answer = answer + each["unit"]
            res.append([question, answer, src])
    return res


def parse_response(response):
    pattern = r"\(\d+\)\s*([^(\)]+)(?=\(\d+\)|$)"
    # 使用findall方法查找所有匹配的部分
    matches = re.findall(pattern, response)

    # 清理每个匹配项的空格
    matches = [match.strip() for match in matches]

    # 返回匹配到的列表
    return matches


def check_exist(question, data):
    for item in data:
        if question.strip() == item[0]:
            return True
    return False


def generate_mcq_scibench(ori_scibench_data, output_dir):
    with open("scibench_ins.txt", "r") as fi:
        ins = ""
        for line in fi.readlines():
            ins += line.strip() + "\n"

    for each in tqdm(ori_scibench_data):
        path = os.path.join(output_dir, each[2] + ".csv")
        if os.path.exists(path):
            data = read_csv_file(path)
        else:
            data = []
        question = each[0]
        if check_exist(question, data):
            print("already exist, skip it")
            continue
        answer = each[1]
        src = each[2]
        inputs = "Question: {}\nCorrect Answer: {}\nThree incorrect answers for the multiple-choice " \
                 "options: ".format(question, answer)
        response = call_gpt_4(client=my_client, instruction=ins, inputs=inputs)
        # response = call_gpt_4(client=my_client, instruction=ins, inputs="")
        options = parse_response(response)
        if len(options) > 3:
            options = options[:3]
            print("options too much", response)
        elif len(options) < 3:
            print("options not enough", options, response)
            continue
        options.append(answer)
        random.shuffle(options)
        idx_map = {0: "A", 1: "B", 2: "C", 3: "D"}
        ans_idx = idx_map[options.index(answer)]
        data.append([question] + options + [ans_idx, src])
        data = deduplicate(data)
        data = sorted(data, key=lambda x: x[0])
        write_2dlist_to_csv(data, path)
        s = 1
    return


def deduplicate(data):
    res = []
    question_map = set()
    for each in data:
        question = each[0]
        if question not in question_map:
            question_map.add(question)
            res.append(each)
        else:
            print("duplicate", each)
    return res


def add_scibench():
    scibench_dir = "/Users/server/MMLU/git/scibench/dataset/original/"
    output_dir = "../experiments/data/add_scibench_mmlu"
    intermediate_mcq_scibench_dir = "../experiments/data/mcq_scibench"
    os.makedirs(output_dir, exist_ok=True)
    os.makedirs(intermediate_mcq_scibench_dir, exist_ok=True)
    scibench_data = load_ori_scibench(scibench_dir)
    generate_mcq_scibench(scibench_data, intermediate_mcq_scibench_dir)


if __name__ == "__main__":
    add_scibench()


