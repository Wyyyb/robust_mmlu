from datasets import load_dataset
from datasets import Dataset
import json


def pull_data():
    dataset = load_dataset("TIGER-Lab/MMLU-Pro")
    test_data, val_data = [], []
    for each in dataset["test"]:
        test_data.append(each)
    for each in dataset["validation"]:
        val_data.append(each)
    with open("local_0518/mmlu_pro_test_data.json", "w") as fo:
        fo.write(json.dumps(test_data))
    with open("local_0518/mmlu_pro_val_data.json", "w") as fo:
        fo.write(json.dumps(val_data))
    return test_data, val_data


def update_data(data):
    with open("/Users/server/MMLU/git/robust_mmlu/ann_data_postprocess/data/ann_modified_data_0520.json",
              "r") as fi:
        modified_data = json.load(fi)
    res = []
    for i, single in enumerate(data):
        check = check_in(single, modified_data)
        if not check:
            res.append(single)
            continue
        if "bad_question" in check and check["bad_question"] is True:
            continue
        check.pop("bad_question")
        res.append(check)
    # res = post_process(res)
    res = remove_na(res)
    return res


def remove_na(data):
    res = []
    for each in data:
        if "N/A" in each["options"]:
            if each["options"][-1] != "N/A":
                print("error")
            temp = []
            for opt in each["options"]:
                if opt != "N/A":
                    temp.append(opt)
            each["options"] = temp
        res.append(each)
    return res


def post_process(data):
    # temp = json.dumps(data)
    # temp = temp.replace("\\textdegree", "°").replace("\textdegree", "°")
    # data = json.loads(temp)
    for i, each in enumerate(data):
        if "\\textdegree" in each["question"]:
            data[i]["question"] = data[i]["question"].replace("\\textdegree", "°")
            print("1111")
        elif "extdegree" in each["question"]:
            data[i]["question"] = data[i]["question"].replace("extdegree", "°")
            print("2222")
        for j, opt in enumerate(each["options"]):
            if "\\textdegree" in opt:
                data[i]["options"][j] = opt.replace("\\textdegree", "°")
                print("3333")
            elif "extdegree" in each["options"]:
                data[i]["options"][j] = opt.replace("extdegree", "°")
                print("4444")
    return data


def check_in(single, modified_data):
    for each in modified_data:
        if single["question_id"] == each["question_id"]:
            if single["question"] == each["question"]:
                return each
            else:
                print("mismatch error")
    return None


def push_data():
    with open("local_0520/mmlu_pro_test_data.json", "r") as fi:
        test_data = json.load(fi)
    with open("local_0520/mmlu_pro_val_data.json", "r") as fi:
        val_data = json.load(fi)
    test_data = update_data(test_data)
    with open("pushed_data/test_data.json", "w") as fo:
        fo.write(json.dumps(test_data))
    print("length of test_data", len(test_data))
    test_dataset = Dataset.from_list(test_data)
    val_dataset = Dataset.from_list(val_data)
    test_dataset.push_to_hub("TIGER-Lab/MMLU-Pro", split="test")
    val_dataset.push_to_hub("TIGER-Lab/MMLU-Pro", split="validation")


if __name__ == "__main__":
    push_data()



