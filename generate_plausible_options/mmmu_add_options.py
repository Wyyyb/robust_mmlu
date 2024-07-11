import openai
import json
import csv
import re
from tqdm import tqdm

openai.api_key = "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"
index_map = {0: "A", 1: "B", 2: "C", 3: "D", 4: "E", 5: "F", 6: "G", 7: "H", 8: "I", 9: "J"}
re_index_map = {"A": 0, "B": 1, "C": 2, "D": 3, "E": 4, "F": 5, "G": 6, "H": 7, "I": 8, "J": 9}


def call_gpt_4(instruction, inputs):
    response = openai.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": instruction + inputs}],
        temperature=0.7,
        max_tokens=2000,
        top_p=0.95,
        frequency_penalty=0,
        presence_penalty=0,
        stop=None
    )
    return response.choices[0].message.content


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


def request_gpt4(question, options, answer):
    instruction = ""
    with open("mmmu_ins.txt", "r", encoding="utf-8") as fi:
        for line in fi.readlines():
            instruction += line + "\n"
    inputs = "Input:\nQuestion: " + question + "\nExisting 4 Options:\n" + options + "\nAnswer: " + answer + \
             "\n\nOutput:\nGenerated 6 distractors (options):\n"
    response = call_gpt_4(instruction, inputs)
    return response


def parse_options(response):
    res = []
    pattern = re.compile(r'^([E-J].).*')
    lines = response.split("\n")
    for line in lines:
        if pattern.match(line):
            res.append(line[2:].strip())
    if len(res) < 6:
        return None
    else:
        return res[:6]


def single_expand(single_item):
    q_id = single_item["id"]
    question = single_item["question"]
    options = single_item["options"]
    if len(options) < 4:
        print("options must be at least 4.\n", options)
        return None
    # return None
    image = single_item.get("image_1", "no images")
    options_str = f"A. {options[0]}\nB. {options[1]}\nC. {options[2]}\nD. {options[3]}"
    answer = single_item["answer"]
    answer_index = re_index_map[answer]
    answer_content = options[answer_index]
    answer_str = f"{answer}. {answer_content}"
    response = request_gpt4(question, options_str, answer_str)
    aug_options = parse_options(response)
    if not aug_options:
        print("parsed fail:\n", response)
        return None
    aug_options_str = f"E. {aug_options[0]}\nF. {aug_options[1]}\nG. {aug_options[2]}\nH. {aug_options[3]}\n" \
                      f"I. {aug_options[4]}\nJ. {aug_options[5]}"
    res = [q_id, question, options_str, answer_str, aug_options_str, image]
    return res


def expand_options():
    input_file = "human_check.json"
    output_file = "augmented_mmmu_sample.csv"
    with open(input_file, "r") as fi:
        input_data = json.load(fi)
    result = [["question_id", "question", "existing options", "answer", "augmented options",
               "image path (if need)"]]
    for i, each in enumerate(tqdm(input_data)):
        # if i > 5:
        #     continue
        curr = single_expand(each)
        if not curr:
            print("skipping")
            continue
        result.append(curr)
    write_2dlist_to_csv(result, output_file)


if __name__ == "__main__":
    expand_options()

