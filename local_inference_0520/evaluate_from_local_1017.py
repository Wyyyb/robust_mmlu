import csv
import json
import argparse
import os
import torch
import numpy as np
import random
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
from transformers import AutoModelForCausalLM
import transformers
import time
import re
from vllm import LLM, SamplingParams
from tqdm import tqdm
from distutils.util import strtobool
import logging
import sys
from datasets import load_dataset

choices = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P"]
max_model_length = 4096
max_new_tokens = 2048


def load_mmlu_pro():
    dataset = load_dataset("TIGER-Lab/MMLU-Pro")
    test_df, val_df = dataset["test"], dataset["validation"]
    test_df = preprocess(test_df)
    val_df = preprocess(val_df)
    return test_df, val_df


def load_mmlu():
    cot_data = read_csv_file("mmlu_cot_data/ori_mmlu-cot.csv")
    test_df, val_df = [], []
    question_id = 0
    for each in cot_data:
        question = each[2]
        category = each[0]
        options = each[3: 7]
        answer = each[7]
        answer_index = options.index(each[8])
        cot_content = each[9]
        curr = {"question_id": question_id, "question": question, "category": category,
                "options": options, "answer": answer, "answer_index": answer_index,
                "cot_content": cot_content, "src": category}
        question_id += 1
        val_df.append(curr)
    for file in os.listdir("mmlu_cot_data/ori_mmlu_data"):
        if not file.endswith(".csv"):
            continue
        file_path = os.path.join("mmlu_cot_data/ori_mmlu_data", file)
        input_data = read_csv_file(file_path)
        category = file.replace("_test.csv", "")
        for each in input_data:
            question = each[0]
            options = each[1: 5]
            answer = each[5]
            answer_index = "ABCDEF".index(answer)
            cot_content = ""
            curr = {"question_id": question_id, "question": question, "category": category,
                    "options": options, "answer": answer, "answer_index": answer_index,
                    "cot_content": cot_content, "src": category}
            question_id += 1
            test_df.append(curr)
    print("mmlu data:\n test_df[0]:\n", test_df[0])
    print("val_df[0]:\n", val_df[0])
    return test_df, val_df


def read_csv_file(file_path):
    with open(file_path, mode='r', encoding='utf-8') as file:
        csv_reader = csv.reader(file)
        data = list(csv_reader)
        if str(data[0][0]) == "0" and str(data[0][1]) == "1" and str(data[0][2]) == "2":
            data = data[1:]
    return data


def load_model():
    try:
        llm = LLM(model=args.model, gpu_memory_utilization=float(args.gpu_util),
                  tensor_parallel_size=args.ngpu, max_model_len=max_model_length,
                  trust_remote_code=True, tokenizer_mode="mistral", config_format="mistral",
                  load_format="mistral")
        sampling_params = SamplingParams(temperature=0.7, top_p=0.95, max_tokens=max_new_tokens,
                                         stop=["Question:"])
        tokenizer = transformers.AutoTokenizer.from_pretrained("/data/yubowang/models/qwen2.5-1.5b",
                                                               trust_remote_code=True)
        # tokenizer = None
    except Exception as e:
        print("vllm unsupported models", e)
        return None, None
    return (llm, sampling_params), tokenizer


def preprocess(test_df):
    res_df = []
    for each in test_df:
        options = []
        for opt in each["options"]:
            if opt == "N/A":
                continue
            options.append(opt)
        each["options"] = options
        res_df.append(each)
    return res_df


def args_generate_path(input_args):
    scoring_method = "CoT"
    model_name = input_args.model.split("/")[-1]
    subjects = args.selected_subjects.replace(",", "-").replace(" ", "_")
    return [model_name, scoring_method, args.dataset]


def select_by_category(df, subject):
    res = []
    for each in df:
        if each["category"] == subject:
            res.append(each)
    return res


def format_cot_example(example, including_answer=True):
    prompt = "Question:\n"
    question = example["question"]
    options = example["options"]
    prompt += question + "\n"
    prompt += "Options:\n"
    for i, opt in enumerate(options):
        prompt += "{}. {}\n".format(choices[i], opt)
    if including_answer:
        cot_content = example["cot_content"].replace("A: Let's think step by step.",
                                                     "Answer: Let's think step by step.")
        prompt += cot_content + "\n\n"
    else:
        prompt += "Answer: "
    return prompt


def generate_cot_prompt(val_df, curr, k):
    prompt = ""
    with open(f"cot_prompt_lib/initial_prompt_0907.txt", "r") as fi:
    # with open(f"cot_prompt_lib/initial_prompt_0908.txt", "r") as fi:
        for line in fi.readlines():
            prompt += line
    subject = curr["category"]
    val_df = select_by_category(val_df, subject)
    val_df = val_df[: k]
    prompt = prompt.replace("{$}", subject) + "\n"
    for example in val_df:
        prompt += format_cot_example(example, including_answer=True)
    prompt += format_cot_example(curr, including_answer=False)
    return prompt


def check_exist(res, q_id):
    for each in res:
        if q_id == each["question_id"]:
            if "pred" in each and each["pred"]:
                # logging.debug("exist, skip it")
                return True
            else:
                logging.debug("no result in exist result error")
                return False
        else:
            continue
    return False


def extract_answer(text):
    pattern = r"answer is \(?([A-J])\)?"
    match = re.search(pattern, text)
    if match:
        return match.group(1)
    else:
        print("1st answer extract failed\n" + text)
        return extract_again(text)


def extract_again(text):
    match = re.search(r'.*[aA]nswer:\s*([A-J])', text)
    if match:
        return match.group(1)
    else:
        return extract_final(text)


def extract_final(text):
    pattern = r"\b[A-J]\b(?!.*\b[A-J]\b)"
    match = re.search(pattern, text, re.DOTALL)
    if match:
        return match.group(0)
    else:
        return None


def batch_inference(llm, sampling_params, inference_batch):
    start = time.time()
    print("---------prompt---------\n", inference_batch[0])
    outputs = llm.generate(inference_batch, sampling_params)
    print("---------generated text---------\n", outputs[0].outputs[0].text)
    logging.info(str(len(inference_batch)) + "size batch costing time: " + str(time.time() - start))
    response_batch = []
    pred_batch = []
    for output in outputs:
        generated_text = output.outputs[0].text
        response_batch.append(generated_text)
        pred = extract_answer(generated_text)
        pred_batch.append(pred)
    return pred_batch, response_batch


def save_res(res, output_path):
    accu, corr, wrong = 0.0, 0.0, 0.0
    with open(output_path, "w") as fo:
        fo.write(json.dumps(res))
    for each in res:
        if not each["pred"]:
            random.seed(12345)
            x = random.randint(0, len(each["options"]) - 1)
            if x == each["answer_index"]:
                corr += 1
                # print("random hit.")
            else:
                wrong += 1
        elif each["pred"] == each["answer"]:
            corr += 1
        else:
            wrong += 1
    if corr + wrong == 0:
        return 0.0, 0.0, 0.0
    accu = corr / (corr + wrong)
    return accu, corr, wrong


@torch.no_grad()
def eval_cot(subject, model, tokenizer, val_df, test_df, output_path, exists_result=None):
    llm, sampling_params = model
    if not exists_result:
        res = []
    else:
        res = exists_result
    print("load exists result length", len(res))
    global choices
    logging.info("evaluating " + subject)
    batch_size = args.batch_size
    inference_batches = []
    in_batch_index = []

    for i in tqdm(range(len(test_df))):
        k = args.ntrain
        options_num = len(test_df[i]["options"])
        if options_num != 10 and options_num != 4:
            print("options_num", options_num)
        curr = test_df[i]
        q_id = curr["question_id"]
        if check_exist(res, q_id):
            continue
        prompt_length_ok = False
        prompt = None
        while not prompt_length_ok:
            prompt = generate_cot_prompt(val_df, curr, k)
            inputs = tokenizer(prompt, return_tensors="pt")
            inputs = {key: value.cuda() for key, value in inputs.items()}
            length = len(inputs["input_ids"][0])
            if length < max_model_length - max_new_tokens:
                prompt_length_ok = True
            k -= 1
        inference_batches.append(prompt)
        in_batch_index.append(i)

    i = 0
    while i < len(test_df):
        if i + batch_size < len(test_df):
            end_index = i + batch_size
        else:
            end_index = len(test_df)
        curr_batch = inference_batches[i: end_index]
        print("i", i)
        print("end_index", end_index)
        try:
            pred_batch, response_batch = batch_inference(llm, sampling_params, curr_batch)
        except Exception as e:
            print("Error", e)
            i += batch_size
            continue
        index_list = in_batch_index[i: end_index]
        for j, index in enumerate(index_list):
            curr = test_df[index]
            curr["pred"] = pred_batch[j]
            curr["generated_text"] = response_batch[j]
            res.append(curr)
        accu, corr, wrong = save_res(res, output_path)
        logging.info("this batch accu is: {}, corr: {}, wrong: {}\n".format(str(accu), str(corr), str(wrong)))
        i += batch_size
    accu, corr, wrong = save_res(res, output_path)
    return accu, corr, wrong


def main():
    model, tokenizer = load_model()
    if not os.path.exists(save_result_dir):
        os.makedirs(save_result_dir)

    if args.dataset == "mmlu":
        full_test_df, full_val_df = load_mmlu()
    else:
        full_test_df, full_val_df = load_mmlu_pro()
    all_subjects = []
    for each in full_test_df:
        if each["category"] not in all_subjects:
            all_subjects.append(each["category"])
    if args.selected_subjects == "all":
        selected_subjects = all_subjects
    else:
        selected_subjects = []
        args_selected = args.selected_subjects.split(",")
        for sub in all_subjects:
            for each in args_selected:
                if each.replace(" ", "_") in sub.replace(" ", "_"):
                    selected_subjects.append(sub)
    logging.info("selected subjects:\n" + "\n".join(selected_subjects))
    print("selected subjects:\n" + "\n".join(selected_subjects))
    sta_dict = {}
    selected_subjects = sorted(selected_subjects)
    with open(os.path.join(summary_path), 'a') as f:
        f.write("\n------category level sta------\n")
    for subject in selected_subjects:
        if subject not in sta_dict:
            sta_dict[subject] = {"corr": 0.0, "wrong": 0.0, "accu": 0.0}
        test_df = select_by_category(full_test_df, subject)
        val_df = select_by_category(full_val_df, subject)
        output_path = os.path.join(save_result_dir, "{}.json".format(subject))
        if os.path.exists(output_path):
            with open(output_path, "r") as fi:
                exists_result = json.load(fi)
        else:
            exists_result = []
        temp = []
        for each in exists_result:
            if not each["pred"]:
                continue
            temp.append(each)
        exists_result = temp
        acc, corr_count, wrong_count = eval_cot(subject, model, tokenizer, val_df,
                                                test_df, output_path, exists_result)
        sta_dict[subject]["corr"] = corr_count
        sta_dict[subject]["wrong"] = wrong_count
        sta_dict[subject]["accu"] = acc
        with open(os.path.join(summary_path), 'a') as f:
            f.write("Average accuracy {:.4f} - {}\n".format(sta_dict[subject]["accu"], subject))
    total_corr, total_wrong = 0.0, 0.0
    for k, v in sta_dict.items():
        total_corr += v["corr"]
        total_wrong += v["wrong"]
    total_accu = total_corr / (total_corr + total_wrong + 0.000001)
    sta_dict["total"] = {"corr": total_corr, "wrong": total_wrong, "accu": total_accu}

    with open(os.path.join(summary_path), 'a') as f:
        f.write("\n------average acc sta------\n")
        weighted_acc = total_accu
        f.write("Average accuracy: {:.4f}\n".format(weighted_acc))
    with open(global_record_file, 'a', newline='') as file:
        writer = csv.writer(file)
        record = args_generate_path(args) + [time_str, weighted_acc]
        writer.writerow(record)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ntrain", "-k", type=int, default=5)
    parser.add_argument("--selected_subjects", "-sub", type=str, default="all")
    parser.add_argument("--ngpu", "-g", type=int, default=1)
    parser.add_argument("--save_dir", "-s", type=str, default="results")
    parser.add_argument("--global_record_file", "-grf", type=str,
                        default="eval_record_collection.csv")
    parser.add_argument("--gpu_util", "-gu", type=str, default="0.8")
    parser.add_argument("--batch_size", "-bs", type=int, default=-1)
    parser.add_argument("--model", "-m", type=str, default="meta-llama/Llama-2-7b-hf")
    parser.add_argument("--dataset", "-d", type=str, default="mmlu-pro")
    parser.add_argument("--answer_extractor", "-ae", type=str, default="normal",
                        choices=["strict", "normal", "lenient"])

    args = parser.parse_args()
    os.makedirs(args.save_dir, exist_ok=True)
    global_record_file = args.global_record_file
    save_result_dir = os.path.join(
        args.save_dir, "/".join(args_generate_path(args))
    )
    file_prefix = "-".join(args_generate_path(args))
    timestamp = time.time()
    time_str = time.strftime('%m-%d_%H-%M', time.localtime(timestamp))
    file_name = f"{file_prefix}_{time_str}_summary.txt"
    summary_path = os.path.join(args.save_dir, "summary", file_name)
    os.makedirs(os.path.join(args.save_dir, "summary"), exist_ok=True)
    os.makedirs(save_result_dir, exist_ok=True)
    save_log_dir = os.path.join(args.save_dir, "log")
    os.makedirs(save_log_dir, exist_ok=True)
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s %(message)s',
                        handlers=[logging.FileHandler(os.path.join(save_log_dir,
                                                                   file_name.replace("_summary.txt",
                                                                                     "_logfile.log"))),
                                  logging.StreamHandler(sys.stdout)])

    main()


