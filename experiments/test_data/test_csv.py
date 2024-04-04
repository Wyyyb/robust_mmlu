import pandas as pd
import csv

def read_csv_file(file_path, start_line=0):
    with open(file_path, mode='r', encoding='utf-8') as file:
        csv_reader = csv.reader(file)
        data = list(csv_reader)
    data = data[start_line:]
    return data


def pandas_read_csv(filename):
    df = pd.read_csv(filename, header=0)
    data = df.values.tolist()
    for each in data:
        if "If I_2 and Br_2 are added to a solution containing " in each[0]:
            print("found, index is", data.index(each))


def csv_read_csv(filename):
    data = read_csv_file(filename)
    for each in data:
        if "If I_2 and Br_2 are added to a solution containing " in each[0]:
            print("found, index is", data.index(each))



pandas_read_csv("/Users/server/MMLU/git/robust_mmlu/experiments/eval_result/symbol_scoring/Llama-2-7b-hf/mmlu_pro/ori_eval/chemistry.csv")

csv_read_csv("/Users/server/MMLU/git/robust_mmlu/experiments/eval_result/symbol_scoring/Llama-2-7b-hf/mmlu_pro/ori_eval/chemistry.csv")



