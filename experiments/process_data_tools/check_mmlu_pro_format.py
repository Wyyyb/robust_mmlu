import csv
import os


def read_csv_file(file_path):
    with open(file_path, mode='r', encoding='utf-8') as file:
        csv_reader = csv.reader(file)
        data = list(csv_reader)
    return data


def write_2dlist_to_csv(data, file_name):
    with open(file_name, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerows(data)


def check_format(mmlu_dir):
    for file in os.listdir(mmlu_dir):
        file_path = os.path.join(mmlu_dir, file)
        data = read_csv_file(file_path)
        res = []
        for each in data:
            if len(each) != 7:
                print(file, "length wrong", len(each))
                print(each)
                continue
            res.append(each)
        # write_2dlist_to_csv(res, file_path)


if __name__ == '__main__':
    check_format("../data/add_stemez_mmlu/")
    # check_format("../data/add_scibench_mmlu")

