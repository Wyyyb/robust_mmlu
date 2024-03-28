import os


def rename_subfolders_with_abc(folder_path):
    # 检查给定的路径是否确实存在且为目录
    if not os.path.isdir(folder_path):
        print("提供的路径不是一个有效的目录")
        return

    try:
        # os.listdir() 返回指定的文件夹包含的文件或文件夹的名字的列表
        for item in os.listdir(folder_path):
            # 构建完整的文件/文件夹路径
            item_path = os.path.join(folder_path, item)
            # 检查这个路径是否为目录
            if os.path.isdir(item_path):
                # 构建新的文件夹名字
                new_folder_name = single_rename(item)
                # 构建新的文件夹完整路径
                new_folder_path = os.path.join(folder_path, new_folder_name)
                # 重命名文件夹
                os.rename(item_path, new_folder_path)
    except Exception as e:
        print(f"重命名过程中发生错误: {e}")


def single_rename(item):
    segments = item.split("_")
    eval_map = {"rare": "rare_symbols", "B": "fix_B", "C": "fix_C"}
    if "ori" in segments:
        dataset_class = "mmlu"
    else:
        dataset_class = "exp_10_mmlu"
    for each in ["rare", "B", "C"]:
        if each in segments:
            eval_class = eval_map[each]
            break
    else:
        eval_class = "ori"
    if "7b" in segments:
        if "chat" in segments:
            model_class = "7b_chat"
        else:
            model_class = "7b"
    else:
        if "chat" in segments:
            model_class = "13b_chat"
        else:
            model_class = "13b"
    res = "-".join([dataset_class, model_class, eval_class])
    return res


if __name__ == '__main__':
    rename_subfolders_with_abc("../eval_result")



