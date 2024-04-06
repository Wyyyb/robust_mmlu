import csv
import os


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


input_dev_dir = "data/ori_mmlu_dev"
input_test_dir = "../experiments/data/ori_mmlu_test_data"
output_dir = "../experiments/data/ori_mmlu_data"

os.makedirs(output_dir, exist_ok=True)

for file in os.listdir(input_dev_dir):
    dev_path = os.path.join(input_dev_dir, file)
    dev_data = read_csv_file(dev_path)
    if len(dev_data) != 5:
        print("file", file, "len(data)", len(dev_data), dev_data)
        dev_data = dev_data[:5]
    file = file.replace("_dev", "_test")
    test_path = os.path.join(input_test_dir, file)
    if not os.path.exists(test_path):
        print("test file not exist", file)
        continue
    test_data = read_csv_file(test_path)
    data = dev_data + test_data

    for i, each in enumerate(data):
        src_file = file.replace("_dev.csv", "")
        src = f"ori_mmlu-{src_file}"
        data[i].append(src)
        if len(data[i]) != 7:
            print("invalid length", file, data[i])
    write_2dlist_to_csv(data, os.path.join(output_dir, file))







