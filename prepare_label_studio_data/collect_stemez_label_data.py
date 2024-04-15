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


def collect():
    res = []
    mmlu_pro_dir = "../experiments/data/images_removed_mmlu"
    stemez_meta_info_dir = "/Users/server/MMLU/git/ScienceEval/mmlu_pro/processed_data/"
    stemez_meta_info = {}
    ref_id = 0
    for file in os.listdir(stemez_meta_info_dir):
        if not file.endswith(".jsonl"):
            continue
        file_path = os.path.join(stemez_meta_info_dir, file)
        with open(file_path, "r") as fi:
            for line in fi.readlines():
                curr_data = json.loads(line)
                src = "stemez-" + file.split("_")[1]
                question = curr_data["question"]
                solution = curr_data["solution"]
                if src not in stemez_meta_info:
                    stemez_meta_info[src] = {}
                if question not in stemez_meta_info[src]:
                    stemez_meta_info[src][question] = []
                stemez_meta_info[src][question].append(solution)

    for file in os.listdir(mmlu_pro_dir):
        if not file.endswith(".csv"):
            continue
        file_path = os.path.join(mmlu_pro_dir, file)
        data = read_csv_file(file_path)
        for each in data:
            question = each[0]
            options = each[1: 5]
            answer = each[5]
            src = each[6]
            task_1 = ""
            if src not in stemez_meta_info:
                continue
            if question not in stemez_meta_info[src]:
                print("question not in stemez_meta_info[src]\n", question)
                continue
            if len(stemez_meta_info[src][question]) != 1:
                solution = "There is no given solution. Please check the question and the answer on your own."
                print("There is no given solution", len(stemez_meta_info[src][question]))
            else:
                solution = stemez_meta_info[src][question][0]
            my_text = f"Question:\n{question}\n\nOptions:\nA. {options[0]}\nB. {options[1]}\nC.\
             {options[2]}\nD. {options[3]}\n\nAnswer: {answer}\n\nReference Solution:\n{solution}"
            meta_info = {"subject": file, "src": src, "question": question, "options": options,
                         "answer": answer, "solution": solution}
            curr_data = {"text": my_text, "ref_id": ref_id, "meta_info": meta_info,
                         "question": "task_1"}
            # curr_data = {"text": text, "ref_id": ref_id}
            ref_id += 1
            res.append({"data": curr_data})
    print("length", len(res))
    # return res[:200]
    return res


if __name__ == "__main__":
    ann_data = collect()
    single_limit = 200
    i = 0
    while i < len(ann_data):
        f_id = i // single_limit
        end = i + single_limit
        if end > len(ann_data):
            end = len(ann_data)
        with open(f"data/stemez_label_data_{str(f_id)}.json", "w", encoding="utf-8") as fo:
            print("start", i, "end", end)
            fo.write(json.dumps(ann_data[i: end]))
        i = end




