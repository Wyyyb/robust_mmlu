import json
import random


def post_process_item(item):
    opts = item["options"]
    answer_idx = item["answer_index"]
    correct_option = opts[answer_idx]
    random.shuffle(opts)
    while opts[answer_idx] == correct_option:
        print("shuffle again")
        random.shuffle(opts)
    new_answer_idx = opts.index(correct_option)
    idx_map = "ABCDEFGHIJ"
    answer = idx_map[new_answer_idx]
    item["options"] = opts
    item["answer_index"] = new_answer_idx
    item["answer"] = answer
    item["question"] = item["question"] + " "
    return item


with open("mmlu_pro_test_data.json", "r") as fi:
    data = json.load(fi)

modified_ids = ["6045", "6249", "6252", "6307", "6308", "6432", "6491", "6493", "6501", "6503", "6507",
                "6550", "6611", "6672"]

exist_data = {}
duplicate_ids = []
du_count = 0
new_data = []
for each in data:
    question = each["question"]
    options = each["options"]
    question_str = question + "\n".join(options)

    if question_str not in exist_data:
        exist_data[question_str] = each["question_id"]
        new_data.append(each)
    else:
        # if str(each["question_id"]) in modified_ids or str(exist_data[question_str]) in modified_ids:
        #     print("modified", each["question_id"], exist_data[question_str])
        # print("q id", each["question_id"], exist_data[question_str])
        duplicate_ids.append(each["question_id"])
        du_count += 1
        new_data.append(post_process_item(each))







