import csv
import os


input_dir = "/Users/server/MMLU/git/robust_mmlu/filter_stemez/data/images_removed_mmlu"
# input_dir = "/Users/server/MMLU/git/robust_mmlu/experiments/data/mmlu_pro_v1"
file_list = list(os.listdir(input_dir))
file_list = sorted(file_list)


def read_csv_file(file_path):
    with open(file_path, mode='r', encoding='utf-8') as file:
        csv_reader = csv.reader(file)
        data = list(csv_reader)
        if str(data[0][0]) == "0" and str(data[0][1]) == "1" and str(data[0][2]) == "2":
            data = data[1:]
    return data


def sta():
    sum_count = 0
    for file in file_list:
        if not file.endswith(".csv"):
            continue
        file_path = os.path.join(input_dir, file)
        data = read_csv_file(file_path)
        sum_count += len(data)
        print(file, len(data))
    print("sum is: ", sum_count)


sta()


