import json
import os

res = []
for file in os.listdir("eval_results"):
    if not file.endswith(".json"):
        continue
    with open(os.path.join("eval_results", file), "r") as fi:
        curr = json.load(fi)
        res += curr

with open(os.path.join("eval_results", "DeepSeek_V2_Coder_result.json"), "w") as fo:
    fo.write(json.dumps(res))






