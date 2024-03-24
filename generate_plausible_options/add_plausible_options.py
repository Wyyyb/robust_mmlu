import os
from openai import AzureOpenAI
import csv
import re
import random
from tqdm import tqdm

API_KEY = '786f8c1ff30a4c4b9f9b8917f2f5191b'

my_client = AzureOpenAI(
  azure_endpoint="https://waterloo-gpt4.openai.azure.com/",
  api_key=API_KEY,
  api_version="2024-02-15-preview"
)


index_map = {0: "A", 1: "B", 2: "C", 3: "D", 4: "E", 5: "F", 6: "G", 7: "H", 8: "I", 9: "J"}
re_index_map = {"A": 0, "B": 1, "C": 2, "D": 3, "E": 4, "F": 5, "G": 6, "H": 7, "I": 8, "J": 9}

skip_files = ['moral_scenarios_test.csv']


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


def write_2dlist_to_csv(data, file_name):
    """
    Write a 2D list to a CSV file.

    Parameters:
        data (list of list of str): The 2D list to be written to the CSV file.
        file_name (str): The name of the CSV file.
    """
    with open(file_name, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerows(data)


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


def request_gpt4(question, options, answer):
    instruction = ""
    with open("ins.txt", "r", encoding="utf-8") as fi:
        for line in fi.readlines():
            instruction += line + "\n"
    inputs = "Input:\nQuestion: " + question + "\nExisting 4 Options:\n" + options + "\nAnswer: " + answer + \
             "\n\nOutput:\nGenerated 6 Options:\n"
    response = call_gpt_4(my_client, instruction, inputs)

    return response


def check_exist(question_str, result):
    for each in result:
        if question_str in each:
            return True
    return False


def parse_options(response):
    res = []
    pattern = re.compile(r'^([E-J]:).*')
    lines = response.split("\n")
    for line in lines:
        if pattern.match(line):
            res.append(line[2:].strip())
    if len(res) < 6:
        return None
    else:
        return res[:6]


def expand_options():
    input_dir = "ori_mmlu_data/"
    output_dir = "expand_10_mmlu_data/"
    os.makedirs(output_dir, exist_ok=True)
    for each_file in os.listdir(input_dir):
        if each_file in skip_files:
            continue
        if os.path.exists(os.path.join(output_dir, each_file)):
            continue
        file_path = os.path.join(input_dir, each_file)
        input_data = read_csv_file(file_path)
        output_data = []
        output_path = os.path.join(output_dir, each_file)
        for i, line in tqdm(enumerate(input_data)):
            if len(line) != 6:
                print("invalid format", i, line)
                continue
            if i > 6:
                continue
            single_out = [line[0]]
            question_str = line[0]
            options = line[1: 5]
            ans_index = line[5]
            answer_content = options[re_index_map[ans_index]]
            options_str = "A: {}\nB: {}\nC: {}\nD: {}".format(options[0], options[1], options[2], options[3])
            answer_str = "{}: {}".format(ans_index, options[re_index_map[ans_index]])
            response = request_gpt4(question_str, options_str, answer_str)
            expanded_options = parse_options(response)
            new_options = options + expanded_options
            random.shuffle(new_options)
            new_ans_index = index_map[new_options.index(answer_content)]
            single_out += new_options + [new_ans_index]
            output_data.append(single_out)
        write_2dlist_to_csv(output_data, output_path)


if __name__ == "__main__":
    expand_options()
















