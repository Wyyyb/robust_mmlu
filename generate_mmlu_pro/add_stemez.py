import csv
import os
import random
import json


def read_csv_file(file_path):
    with open(file_path, mode='r', encoding='utf-8') as file:
        csv_reader = csv.reader(file)
        data = list(csv_reader)
    return data


def write_2dlist_to_csv(data, file_name):
    with open(file_name, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerows(data)


stemez_cat_map = {
    "engineer_AutomaticControlSystemsRobotics_stemez.jsonl": "engineering.csv",
    "engineer_ElectricalMachines_stemez.jsonl": "engineering.csv",
    "engineer_ElectricCircuits_stemez.jsonl": "engineering.csv",
    "engineer_Electromagnetics_stemez.jsonl": "engineering.csv",
    "engineer_ElectronicCommunications_stemez.jsonl": "engineering.csv",
    "engineer_FluidMechanics_stemez.jsonl": "engineering.csv",
    "engineer_HeatTransfer_stemez.jsonl": "engineering.csv",
    "engineer_MachineDesign_stemez.jsonl": "engineering.csv",
    "engineer_StrengthofMaterials_stemez.jsonl": "engineering.csv",
    "engineer_Thermodynamics_stemez.jsonl": "engineering.csv",
    "engineer_TransportPhenomena_stemez.jsonl": "engineering.csv",
    "science_Biology_stemez.jsonl": "biology.csv",
    "science_Business_stemez.jsonl": "business.csv",
    "science_Chemistry_stemez.jsonl": "chemistry.csv",
    "science_ComputerScience_stemez.jsonl": "computer science.csv",
    "science_Economics_stemez.jsonl": "economics.csv",
    "science_Genetics_stemez.jsonl": "biology.csv",
    "science_Mechanics_stemez.jsonl": "physics.csv",
    "science_Optics_stemez.jsonl": "physics.csv",
    "science_OrganicChemistry_stemez.jsonl": "chemistry.csv",
    "science_PhysicalChemistry_stemez.jsonl": "chemistry.csv",
    "science_Physics_stemez.jsonl": "physics.csv",
    "science_Psychology_stemez.jsonl": "psychology.csv"}

idx_map = {0: "A", 1: "B", 2: "C", 3: "D"}

stemez_list = []

for k, v in stemez_cat_map.items():
    if v not in stemez_list:
        stemez_list.append(v)

output_dir = "../experiments/data/add_stemez_mmlu"
stemez_dir = "../experiments/data/stemez_data"
exist_mmlu_dir = "../experiments/data/add_scibench_mmlu"

os.makedirs(output_dir, exist_ok=True)

stemez_data_map = {}

for file in os.listdir(exist_mmlu_dir):
    if file.endswith("csv") and file not in stemez_list:
        data = read_csv_file(os.path.join(exist_mmlu_dir, file))
        write_2dlist_to_csv(data, os.path.join(output_dir, file))
    elif file.endswith("csv") and file in stemez_list:
        data = read_csv_file(os.path.join(exist_mmlu_dir, file))
        print("ori dataset length", file, len(data))
        stemez_data_map[file] = data


def check_stemez(single_data):
    lack_data_list = ["science_ComputerScience_stemez.jsonl", "science_Psychology_stemez.jsonl",
                      "science_Biology_stemez.jsonl", "science_Genetics_stemez.jsonl"]
    if single_data["image_question"] or single_data["image_answer"]:
        return False
    if not single_data["short_answer"] and single_data["filename"] not in lack_data_list:
        return False
    if not single_data["short_answer"] and single_data["filename"] in lack_data_list and \
            len(single_data["answer"]) > 268:
        return False
    return True


for file in os.listdir(stemez_dir):
    if not file.startswith("stemez"):
        continue
    file_path = os.path.join(stemez_dir, file)
    data = []
    with open(file_path, "r") as fi:
        for line in fi.readlines():
            line = line.replace("plausible_answers", "plausible answers")
            data.append(json.loads(line))
    for each in data:
        if not check_stemez(each):
            continue
        src_file = each["filename"]
        target_file = stemez_cat_map[src_file]
        src = each["src"]
        question = each["question"]
        if "plausible answers" not in each:
            print("plausible answers not in each", each)
            continue
        if len(each["plausible answers"]) > 3:
            each["plausible answers"] = each["plausible answers"][:3]
        elif len(each["plausible answers"]) < 3:
            continue
        options = each["plausible answers"] + [each["answer"]]
        random.shuffle(options)
        answer_idx = idx_map[options.index(each["answer"])]
        curr_res = [question] + options + [answer_idx, src]
        stemez_data_map[target_file].append(curr_res)

for k, v in stemez_data_map.items():
    print("augmented dataset length", k, len(v))
    write_2dlist_to_csv(v, os.path.join(output_dir, k))

