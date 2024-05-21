import os
import json

output_dir = "eval_results_processed_0521/"
os.makedirs(output_dir, exist_ok=True)

for each_dir in os.listdir("eval_results_mmlu_pro_0521"):
    if each_dir.startswith("."):
        continue
    dir_path = os.path.join("eval_results_mmlu_pro_0521", each_dir)
    output_file_name = os.path.join(output_dir, "model_outputs_" + each_dir + "_5shots" + ".json")
    data = []
    for each_file in os.listdir(dir_path):
        if each_file.startswith("."):
            continue
        file_path = os.path.join(dir_path, each_file)
        with open(file_path, "r") as fi:
            curr = json.load(fi)
            data += curr
    res = sorted(data, key=lambda x: x["question_id"])
    with open(output_file_name, "w") as fo:
        fo.write(json.dumps(res))












