import os


def find_csv_filenames(dir_path):
    """
    This function returns a list of .csv filenames in the given directory
    :param dir_path: the path of the directory to search
    :return: a list of .csv filenames found in the given directory
    """
    csv_files = []
    # 检查路径是否存在
    if not os.path.isdir(dir_path):
        print("The directory does not exist.")
        return csv_files

    # 遍历目录中的所有文件和子目录
    for entry in os.listdir(dir_path):
        # 拼接完整的文件路径
        full_path = os.path.join(dir_path, entry)
        # 检查是否为文件并且文件名以.csv结尾
        if os.path.isfile(full_path) and entry.endswith('.csv'):
            csv_files.append(entry.replace("_test.csv", ""))

    return csv_files


# 示例用法
dir_path = '../data/ori_mmlu_data'
csv_files = find_csv_filenames(dir_path)
print(",".join(csv_files))








