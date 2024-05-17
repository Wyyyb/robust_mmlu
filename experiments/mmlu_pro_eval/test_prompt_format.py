import json
from prompt_format_examples import prompt_format_examples_0516


with open("../../data/ori_mmlu_data_json/college_physics.json", "r") as fi:
    data = json.load(fi)

each = data[5]
question = each["question"]
options = each["options"]
for i in range(200):
    print("prompt format: ", i, "\n")
    res = prompt_format_examples_0516(i, question, options)
    print(res + "\n----------------------\n")



