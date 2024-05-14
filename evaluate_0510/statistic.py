import json
import os

questions_num = {"biology": 722,
                 "business": 796,
                 "chemistry": 1143,
                 "computer science": 418,
                 "economics": 861,
                 "engineering": 972,
                 "health": 825,
                 "history": 390,
                 "law": 1120,
                 "math": 1357,
                 "other": 942,
                 "philosophy": 511,
                 "physics": 1312,
                 "psychology": 818}


def sta(input_dir, pad=False):
    sta_map = {}
    total_corr = 0.0
    total_wrong = 0.0
    for file in os.listdir(input_dir):
        if not file.endswith(".json") or "summary" not in file:
            continue
        file_path = os.path.join(input_dir, file)
        with open(file_path, "r") as fi:
            curr = json.load(fi)
            for k, v in curr.items():
                if k == "total":
                    continue
                if k in sta_map:
                    print("repeated subjects in different summary files!", k)
                    continue
                if k not in questions_num:
                    print("subject not in questions nums map", k)
                    continue
                corr = v["corr"]
                wrong = v["wrong"]
                if pad:
                    corr += (questions_num[k] - (corr + wrong)) // 10
                    wrong = questions_num[k] - corr
                v["corr"] = corr
                v["wrong"] = wrong
                v["acc"] = corr / (corr + wrong)
                sta_map[k] = v
                total_corr += corr
                total_wrong += wrong
    sta_map["total"] = {"corr": total_corr, "wrong": total_wrong,
                        "acc": total_corr / (total_corr + total_wrong)}
    print("sta result: ", sta_map)
    sta_result_path = os.path.join(input_dir, "sta_result.json")
    with open(sta_result_path, "w") as fo:
        fo.write(json.dumps(sta_map))


if __name__ == "__main__":
    cot_result_dir = "../experiments/eval_result_0510_gpt_4_cot"
    wo_cot_result_dir = "../experiments/eval_result_0510_gpt_4"
    # sta(cot_result_dir)
    sta(wo_cot_result_dir)








