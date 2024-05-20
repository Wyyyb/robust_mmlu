import json


def statistic():
    # with open("mmlu_pro_data_v1/mmlu_pro_test.json", "r") as fi:
    with open("/Users/server/MMLU/git/robust_mmlu/data_hf/local_0521/mmlu_pro_test_data.json", "r") as fi:
        data = json.load(fi)
    cat_data, src_data = {}, {}
    cat_src_data = {}
    src_map = {"ori_mmlu": "Original MMLU Questions",
               "stemez": "STEM Website",
               "theoremQA": "TheoremQA",
               "scibench": "Scibench"}
    for each in data:
        for key, value in src_map.items():
            if key in each["src"]:
                if value not in src_data:
                    src_data[value] = 1
                else:
                    src_data[value] += 1
        if each["category"] not in cat_data:
            cat_data[each["category"]] = 1
            cat_src_data[each["category"]] = {"ori": 0, "new": 0}
        else:
            cat_data[each["category"]] += 1
        if "ori_mmlu" in each["src"]:
            cat_src_data[each["category"]]["ori"] += 1
        else:
            cat_src_data[each["category"]]["new"] += 1

    print("cat_data", cat_data)
    print("src_data", src_data)
    print("cat_src_data", cat_src_data)
    return cat_data, src_data


def display_cat():
    return


def display_src():
    return


def main():
    cat_data, src_data = statistic()
    display_cat()
    display_src()


if __name__ == '__main__':
    main()
