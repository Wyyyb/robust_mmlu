from openai import AzureOpenAI
import json
from tqdm import tqdm
import random
import os
import time
import csv
random.seed(268)
API_KEY = '786f8c1ff30a4c4b9f9b8917f2f5191b'

my_client = AzureOpenAI(
  azure_endpoint="https://waterloo-gpt4.openai.azure.com/",
  api_key=API_KEY,
  api_version="2024-02-15-preview"
)


subcategories = {
    "biology.csv": "biology",
    "business.csv": "business",
    "chemistry.csv": "chemistry",
    "computer science.csv": "computer science",
    "culture.csv": "culture",
    "economics.csv": "economics",
    "engineering.csv": "engineering",
    "geography.csv": "geography",
    "health.csv": "health",
    "history.csv": "history",
    "law.csv": "law",
    "math.csv": "math",
    "other.csv": "other",
    "philosophy.csv": "philosophy",
    "physics.csv": "physics",
    "politics.csv": "politics",
    "psychology.csv": "psychology"
}


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


def translate_single_by_gpt4(text):
    prompt = "将这道英文题目及其选项翻译为中文："
    try:
        start = time.time()
        response = my_client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": text}],
            temperature=0.7,
            timeout=60
        )
        print("request using time", time.time() - start)
        output = response.choices[0].message.content
    except Exception as e:
        print("e", e)
        output = "None"
    return output


def check_exist(res, request):
    for each in res:
        if request in each:
            return True
    return False


def check_mmlu_pro_quality(input_dir, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, "sample_0406.csv")
    res = []
    if os.path.exists(output_path):
        res = read_csv_file(output_path)
    subject_count = {}
    temp = []
    for each in res:
        if each[3] == "None":
            print("found None", each)
            continue
        if each[0] not in subject_count:
            subject_count[each[0]] = 1
        else:
            if subject_count[each[0]] >= 100:
                print("exceed 100, abandon it")
                continue
            else:
                subject_count[each[0]] += 1
        temp.append(each)
    print("loading existing subjects", subject_count)
    res = temp
    file_list = list(os.listdir(input_dir))
    file_list = sorted(file_list)
    for file in file_list:
        print("file", file)
        file_path = os.path.join(input_dir, file)
        data = read_csv_file(file_path)
        random.shuffle(data)
        for i in tqdm(range(100)):
            if len(data) <= i:
                continue
            answer = data[i][5]
            src = data[i][6]
            subject = file

            if subject in subject_count and subject_count[subject] >= 100:
                continue
            question = data[i][0]

            request = f"{question}\nA. {data[i][1]}\nB. {data[i][2]}\nC. {data[i][3]}\nD. {data[i][4]}\n"
            if check_exist(res, request):
                # print("already exist, skip it", request)
                continue
            trans_res = translate_single_by_gpt4(request)
            res.append([subject, src, request, trans_res, answer])
            res = sorted(res, key=lambda x: x[0])
            if subject not in subject_count:
                subject_count[subject] = 1
            else:
                subject_count[subject] += 1
            write_2dlist_to_csv(res, output_path)


if __name__ == "__main__":
    mmlu_pro_dir = "../experiments/data/mmlu_pro_v1/"
    result_dir = "data/translate_0406/"
    check_mmlu_pro_quality(mmlu_pro_dir, result_dir)

