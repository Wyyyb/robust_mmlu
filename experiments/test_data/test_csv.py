import pandas as pd
import csv


def read_csv_file(file_path, start_line=0):
    with open(file_path, mode='r', encoding='utf-8') as file:
        csv_reader = csv.reader(file)
        data = list(csv_reader)
    data = data[start_line:]
    return data


def pandas_read_csv(filename, start_line=-1):
    if start_line == 1:
        df = pd.read_csv(filename, header=0)
    else:
        df = pd.read_csv(filename, header=None)
    data = df.values.tolist()
    # for each in data:
    #     if "If I_2 and Br_2 are added to a solution containing " in each[0]:
    #         print("found, index is", data.index(each))
    return data


def csv_read_csv(filename):
    data = read_csv_file(filename)
    # for each in data:
    #     if "If I_2 and Br_2 are added to a solution containing " in each[0]:
    #         print("found, index is", data.index(each))
    return data

ori_chemistry = "/Users/server/MMLU/git/robust_mmlu/experiments/data/mmlu_pro_v0_1/chemistry.csv"
chemistry = "/Users/server/MMLU/git/robust_mmlu/experiments/eval_result/symbol_scoring/Llama-2-7b-hf/mmlu_pro/ori_eval/chemistry.csv"


res = read_csv_file(ori_chemistry)
ori = pandas_read_csv(ori_chemistry)
# ori = ori[5:]

for i in range(len(ori)):
    if ori[i][0] != res[i][0]:
        s = 1

print("s")






