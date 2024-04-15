import json
import os


def split_json_file(file_path):
    # 确保输入文件存在
    if not os.path.isfile(file_path):
        print(f"文件 {file_path} 不存在。")
        return

    # 加载 JSON 文件内容
    with open(file_path, 'r', encoding='utf-8') as file:
        json_data = json.load(file)

    # 确保 JSON 数据是 list
    if not isinstance(json_data, list):
        print(f"JSON 文件的内容不是 list。")
        return

    # 找到分割点
    split_index = len(json_data) // 2

    # 分割 JSON 数据
    json_data_1 = json_data[:split_index]
    json_data_2 = json_data[split_index:]

    # 获取不带扩展名的文件名称
    base_name = os.path.splitext(os.path.basename(file_path))[0]

    # 创建两个新的 JSON 文件路径
    file_path_1 = os.path.join(os.path.dirname(file_path), f"{base_name}_part1.json")
    file_path_2 = os.path.join(os.path.dirname(file_path), f"{base_name}_part2.json")

    # 保存第一部分
    with open(file_path_1, 'w', encoding='utf-8') as file:
        json.dump(json_data_1, file, ensure_ascii=False, indent=4)
        print(f"第一部分已保存至 {file_path_1}")

    # 保存第二部分
    with open(file_path_2, 'w', encoding='utf-8') as file:
        json.dump(json_data_2, file, ensure_ascii=False, indent=4)
        print(f"第二部分已保存至 {file_path_2}")


# 示例使用：
file_path = 'data/stemez_label_data_10.json'
split_json_file(file_path)


