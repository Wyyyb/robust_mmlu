import csv
import os


subcategories = {
    "abstract_algebra": ["math"],
    "anatomy": ["health"],
    "astronomy": ["physics"],
    "business_ethics": ["business"],
    "clinical_knowledge": ["health"],
    "college_biology": ["biology"],
    "college_chemistry": ["chemistry"],
    "college_computer_science": ["computer science"],
    "college_mathematics": ["math"],
    "college_medicine": ["health"],
    "college_physics": ["physics"],
    "computer_security": ["computer science"],
    "conceptual_physics": ["physics"],
    "econometrics": ["economics"],
    "electrical_engineering": ["engineering"],
    "elementary_mathematics": ["math"],
    "formal_logic": ["philosophy"],
    "global_facts": ["other"],
    "high_school_biology": ["biology"],
    "high_school_chemistry": ["chemistry"],
    "high_school_computer_science": ["computer science"],
    "high_school_european_history": ["history"],
    "high_school_geography": ["geography"],
    "high_school_government_and_politics": ["politics"],
    "high_school_macroeconomics": ["economics"],
    "high_school_mathematics": ["math"],
    "high_school_microeconomics": ["economics"],
    "high_school_physics": ["physics"],
    "high_school_psychology": ["psychology"],
    "high_school_statistics": ["math"],
    "high_school_us_history": ["history"],
    "high_school_world_history": ["history"],
    "human_aging": ["health"],
    "human_sexuality": ["culture"],
    "international_law": ["law"],
    "jurisprudence": ["law"],
    "logical_fallacies": ["philosophy"],
    "machine_learning": ["computer science"],
    "management": ["business"],
    "marketing": ["business"],
    "medical_genetics": ["health"],
    "miscellaneous": ["other"],
    "moral_disputes": ["philosophy"],
    "moral_scenarios": ["philosophy"],
    "nutrition": ["health"],
    "philosophy": ["philosophy"],
    "prehistory": ["history"],
    "professional_accounting": ["other"],
    "professional_law": ["law"],
    "professional_medicine": ["health"],
    "professional_psychology": ["psychology"],
    "public_relations": ["politics"],
    "security_studies": ["politics"],
    "sociology": ["culture"],
    "us_foreign_policy": ["politics"],
    "virology": ["health"],
    "world_religions": ["philosophy"]
}


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


def merge_mmlu(mmlu_dir, output_dir):
    global_map = {}
    mmlu_map = {}
    for each in os.listdir(mmlu_dir):
        if not each.endswith("_test.csv"):
            continue
        # for each_exclude in exclude_files:
        #     if each_exclude in each:
        #         continue
        data = []
        temp_data = read_csv_file(os.path.join(mmlu_dir, each))
        for row in temp_data:
            question = "\t".join(row[:5])
            if question not in global_map:
                global_map[question] = each
                row.append("ori_mmlu-" + each.replace("_test.csv", ""))
                data.append(row)
            else:
                print("duplicate questions", question)
                print(global_map[question], each)
        sub_cat = each.replace("_test.csv", "")
        if sub_cat not in subcategories:
            print("not in subcat", sub_cat)
            continue
        cat = subcategories[sub_cat][0]
        if cat not in mmlu_map:
            mmlu_map[cat] = {sub_cat: data}
        elif sub_cat not in mmlu_map[cat]:
            mmlu_map[cat][sub_cat] = data
        else:
            print("duplicate sub cat", sub_cat)
            continue
    merged_mmlu = {}
    for k, v in mmlu_map.items():
        curr_data = []
        for sub_cat, value in v.items():
            curr_data += value
        merged_mmlu[k] = curr_data
    save_dataset(output_dir, merged_mmlu)
    sta_csv = []
    cat_keys = mmlu_map.keys()
    cat_keys = sorted(cat_keys)
    for each in cat_keys:
        cat_num = 0
        sub_cat_keys = mmlu_map[each].keys()
        sub_cat_keys = sorted(sub_cat_keys)
        for each_key in sub_cat_keys:
            sub_cat_num = len(mmlu_map[each][each_key])
            cat_num += sub_cat_num
        for each_key in sub_cat_keys:
            sta_csv.append([each_key, len(mmlu_map[each][each_key]), each, cat_num])
    write_2dlist_to_csv(sta_csv, os.path.join(output_dir, "../merged_mmlu_sta.csv"))
    return


def save_dataset(dir_path, data_map):
    os.makedirs(dir_path, exist_ok=True)
    for cat, value in data_map.items():
        write_2dlist_to_csv(value, os.path.join(dir_path, cat + ".csv"))


if __name__ == "__main__":
    merge_mmlu("../data/ori_mmlu_data", "../data/merged_mmlu/")




