import csv
import os

exclude_files = ["moral_scenarios"]


def read_csv_file(file_path):
    """
    This function reads a CSV file and returns the data as a list of rows.
    Each row is a list of values.

    :param file_path: The path to the CSV file to read.
    :return: A list of rows, where each row is a list of values.
    """
    with open(file_path, mode='r', encoding='utf-8') as file:
        csv_reader = csv.reader(file)
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


def load_pred_result(dir_path):
    duplicate_map = {}
    pred_result = {}
    for each in os.listdir(dir_path):
        if each.startswith("mmlu") and "fix" not in each:
            path = os.path.join(dir_path, each)
            for root, dirs, files in os.walk(path):
                for file in files:
                    if file.endswith(".csv"):
                        file_path = os.path.abspath(os.path.join(root, file))
                        data = read_csv_file(file_path)
                        model_name = each
                        for i, row in enumerate(data):
                            if i == 0:
                                continue
                            question = "\n".join(row[:5])
                            result = True if row[6] == "True" else False
                            if question not in pred_result:
                                pred_result[question] = {model_name: result}
                            elif model_name not in pred_result[question]:
                                pred_result[question][model_name] = result
                            else:
                                if question not in duplicate_map:
                                    duplicate_map[question] = 1
                                else:
                                    duplicate_map[question] += 1
                                continue
    return pred_result


def trim_down(dir_path, output_dir, model_num):
    k = model_num
    os.makedirs(output_dir, exist_ok=True)
    sta_map = {}
    pred_result = load_pred_result("../eval_result/0328_01_result/")
    for each in os.listdir(dir_path):
        if each not in sta_map:
            sta_map[each] = {}
        for i in range(k + 1):
            sta_map[each][i] = 0
        if each in exclude_files:
            continue
        file_path = os.path.join(dir_path, each)
        data = read_csv_file(file_path)
        curr_output = []
        for row in data:
            question = "\n".join(row[:5])
            if question not in pred_result:
                curr_output.append(row)
                sta_map[each][0] += 1
            else:
                keep, count = trim_judge(pred_result[question])
                if count not in sta_map[each]:
                    print("count exceed", count)
                else:
                    sta_map[each][count] += 1
                if keep:
                    curr_output.append(row)
        write_2dlist_to_csv(curr_output, os.path.join(output_dir, each))
    output_sta_map(sta_map, output_dir, k)


def output_sta_map(sta_map, output_dir, k):
    res = []
    path = os.path.join(output_dir, "../trim_down_sta.csv")
    cats = sta_map.keys()
    cats = sorted(cats)
    for each in cats:
        temp = 0
        for i in range(k + 1):
            temp += sta_map[each][i]
            if i == 0:
                res.append([each, str(i), temp])
            else:
                res.append(["", str(i), temp])
    write_2dlist_to_csv(res, path)


def trim_judge(single_pred_result):
    count = 0
    for k, v in single_pred_result.items():
        if v:
            count += 1
    if count <= 4:
        return True, count
    else:
        return False, count


if __name__ == '__main__':
    trim_down("../data/merged_mmlu/", "../data/trim_down_mmlu/", model_num=8)


