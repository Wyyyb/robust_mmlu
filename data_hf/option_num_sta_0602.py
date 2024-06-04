import json


with open("local_0524/mmlu_pro_test_data.json", "r") as fi:
    data = json.load(fi)

sta_map = {}
for each in data:
    opt_num = len(each["options"])
    if opt_num < 4:
        print("each", each)
    if opt_num not in sta_map:
        sta_map[opt_num] = 0
    sta_map[opt_num] += 1

print("sta_map", sta_map)




