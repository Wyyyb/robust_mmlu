import csv
import os

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


def rare_symbol(input_dir, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    for each_file in os.listdir(input_dir):
        if not each_file.endswith('.csv'):
            continue
        file_path = os.path.join(input_dir, each_file)
        output_path = os.path.join(output_dir, each_file)
        input_data = read_csv_file(file_path)



def fixed_answer_mmlu(input_dir, output_dir):
    os.makedirs(output_dir, exist_ok=True)


def add_perturbations():
    rare_symbol("../experiments/data/ori_mmlu_data", "rare_symbol_mmlu")
    rare_symbol("../experiments/generate_plausible_options/expand_10_mmlu_data",
                "rare_symbol_mmlu_exp_10")
    fixed_answer_mmlu("../experiments/data/ori_mmlu_data", "fixed_answer_mmlu")
    fixed_answer_mmlu("../experiments/generate_plausible_options/expand_10_mmlu_data",
                      "fixed_answer_mmlu_exp_10")


if __name__ == '__main__':
    add_perturbations()

