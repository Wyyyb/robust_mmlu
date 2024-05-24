import os
import json

src_map = {"ori_mmlu": "Original MMLU Questions",
           "stemez": "STEM Website",
           "theoremQA": "TheoremQA",
           "scibench": "Scibench"}


issue_map = {"incorrect answer": ["answer_is_incorrect.json"],
             "bad question": ["bad_questions.json", "meta_options_issue.json"],
             "false negative options": ["duplicate_correct_answer.json",
                                        "hard_to_verify.json",
                                        "question_unsure.json",
                                        "unsure_options.json"]}

re_issue_map = {}
for k, v in issue_map.items():
    for each in v:
        re_issue_map[each] = k

res_map = {}
for file in os.listdir("ann_tag_data/"):
    if not file.endswith(".json") or file not in re_issue_map:
        continue
    with open(os.path.join("ann_tag_data", file), "r") as fi:
        curr = json.load(fi)
    issue_type = re_issue_map[file]
    if issue_type not in res_map:
        res_map[issue_type] = {}

    for each in curr:
        src = ""
        for k, v in src_map.items():
            if k in each["meta_info"]["src"]:
                src = v
                break
        if src not in res_map[issue_type]:
            res_map[issue_type][src] = 0
        res_map[issue_type][src] += 1


print("res_map", res_map)








