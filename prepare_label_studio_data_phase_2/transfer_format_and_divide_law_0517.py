import json
import csv
import os


def read_csv_file(file_path):
    with open(file_path, mode='r', encoding='utf-8') as file:
        csv_reader = csv.reader(file)
        data = list(csv_reader)
        if str(data[0][0]) == "0" and str(data[0][1]) == "1" and str(data[0][2]) == "2":
            data = data[1:]
    return data


def load_mmlu_pro():
    input_dir = "../experiments/data/mmlu_pro_exp_10_options"
    mmlu_pro_data = []
    ref_id = 0
    for file in os.listdir(input_dir):
        if not file.endswith(".csv"):
            continue
        file_path = os.path.join(input_dir, file)
        subject = file
        if "law" not in subject:
            continue
        data = read_csv_file(file_path)
        for each in data:
            if len(each) != 13:
                print("invalid length", len(each), each)
            curr_res = {}
            question = each[0]
            options = each[1:11]
            answer = each[11]
            src = each[12]
            symbol_str = "ABCDEFGHIJ"
            options_str = ""
            for i in range(10):
                options_str += symbol_str[i] + ". " + options[i] + "\n"
            text = f"Question:\n{question}\n\nOptions:\n{options_str}\nAnswer: {answer}"
            meta_info = {"subject": subject, "src": src, "question": question, "options": options,
                         "answer": answer, }
            curr_res = {"text": text, "ref_id": ref_id, "meta_info": meta_info}
            ref_id += 1
            mmlu_pro_data.append(curr_res)
    return mmlu_pro_data


def transfer_and_divide():
    ann_data = load_mmlu_pro()
    single_limit = 200
    i = 0
    while i < len(ann_data):
        f_id = i // single_limit
        end = i + single_limit
        if end > len(ann_data):
            end = len(ann_data)
        with open(f"law_data/phase_3_data_{str(f_id)}.json", "w", encoding="utf-8") as fo:
            print("start", i, "end", end)
            fo.write(json.dumps(ann_data[i: end]))
        i = end


if __name__ == "__main__":
    transfer_and_divide()

