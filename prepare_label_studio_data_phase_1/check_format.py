import json


def compare_json_keys(file_path1, file_path2):
    # 加载 JSON 文件内容
    with open(file_path1, 'r', encoding='utf-8') as file:
        json_data1 = json.load(file)

    with open(file_path2, 'r', encoding='utf-8') as file:
        json_data2 = json.load(file)

    # 递归比较函数
    def compare_dicts(dict1, dict2, path=""):
        keys1 = set(dict1.keys())
        keys2 = set(dict2.keys())

        # 获取两个字典的键差异
        diff_keys1 = keys1 - keys2
        diff_keys2 = keys2 - keys1

        if diff_keys1 or diff_keys2:
            print(f"Path: {path}")
            if diff_keys1:
                print(f"Keys in first JSON only: {diff_keys1}")
            if diff_keys2:
                print(f"Keys in second JSON only: {diff_keys2}")
        else:
            print(keys1, keys2)

        # 对于两个字典中都存在的键，如果值仍然是字典，则递归比较
        for key in keys1.intersection(keys2):
            if isinstance(dict1[key], dict) and isinstance(dict2[key], dict):
                new_path = f"{path}.{key}" if path else key
                compare_dicts(dict1[key], dict2[key], new_path)

    # 比较两个 JSON 数据的每个项目
    for item1, item2 in zip(json_data1, json_data2):
        if isinstance(item1, dict) and isinstance(item2, dict):
            compare_dicts(item1, item2)


# 示例使用：
file_path_1 = 'data/stemez_label_data_1.json'
file_path_2 = 'data/stemez_label_data_5.json'
compare_json_keys(file_path_1, file_path_2)