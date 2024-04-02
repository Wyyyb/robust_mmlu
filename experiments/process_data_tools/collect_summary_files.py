import os
import time


def find_summary_files(directory):
    summary_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file == 'summary.txt':
                summary_files.append(os.path.join(root, file))
    return summary_files


def collect_summary_files(directory):
    timestamp = time.time()
    time_str = time.strftime('%Y-%m-%d_%H-%M-%S', time.localtime(timestamp))
    log_file_name = f"../eval_summary/log_{time_str}.txt"
    paths = find_summary_files(directory)
    res = []
    for each in paths:
        res_path, res_summary = fetch_single_summary(each)
        k = 36 - len(res_path)
        res.append(res_path + " "*k + res_summary)
    res = sorted(res)
    with open(log_file_name, "w") as fo:
        fo.write("\n".join(res))


def fetch_single_summary(summary_path):
    path_segments = str(summary_path).split("/")
    res_path = []
    for each in path_segments:
        if "mmlu" in each:
            res_path.append(each)
    summary_line = -1
    with open(summary_path, "r") as fi:
        for i, line in enumerate(fi.readlines()):
            if i == summary_line:
                return "/".join(res_path), line.strip()
            if "------average acc sta------" in line:
                summary_line = i + 1
    return None, None


if __name__ == "__main__":
    collect_summary_files("../eval_result/")






