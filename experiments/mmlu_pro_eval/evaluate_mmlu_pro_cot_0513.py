import csv
import json
import argparse
import os
import torch
import numpy as np
import random
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
from transformers import AutoModelForCausalLM
from categories import subcategories, categories
from ori_mmlu_categories import ori_mmlu_categories, ori_mmlu_subcategories
import transformers
import time
import re
from vllm import LLM, SamplingParams
from tqdm import tqdm
from distutils.util import strtobool
import logging
import sys
from prompt_format_examples import prompt_format_examples


IGNORE_INDEX = -100
DEFAULT_PAD_TOKEN = "[PAD]"
DEFAULT_EOS_TOKEN = "</s>"
DEFAULT_BOS_TOKEN = "<s>"
DEFAULT_UNK_TOKEN = "<unk>"

choices = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P"]
index_map = {0: "A", 1: "B", 2: "C", 3: "D", 4: "E", 5: "F", 6: "G", 7: "H", 8: "I", 9: "J",
             10: "K", 11: "L", 12: "M", 13: "N", 14: "O", 15: "P"}
re_index_map = {"A": 0, "B": 1, "C": 2, "D": 3, "E": 4, "F": 5, "G": 6, "H": 7, "I": 8, "J": 9,
                "K": 10, "L": 11, "M": 12, "N": 13, "O": 14, "P": 15}


def format_subject(subject):
    return subject.replace(".json", "").replace("_", " ").replace(".csv", "")


def format_example(df, idx, include_answer=True):
    prompt_format = args.prompt_format
    options = df[idx]["options"]
    question = df[idx]["question"]
    prompt = prompt_format_examples(prompt_format, question, options)
    if include_answer:
        ans_index = df[idx]["answer_index"]
        if args.scoring_method == "symbol_scoring":
            prompt += "{}\n\n".format(choices[ans_index])
            if args.prompt_format in [6]:
                prompt += "{}. {}\n\n".format(choices[ans_index], options[ans_index])
        elif args.scoring_method == "hybrid_scoring":
            prompt += "{}\n\n".format(options[ans_index])
    # if idx <= 5:
    #     logging.info("prompt: \n" + prompt)
    return prompt, options


def fix_answer(test_df, fixed_index):
    res = []
    for each in test_df:
        # print("ori", each)
        ans_index = each["answer_index"]
        if ans_index != fixed_index:
            options = each["options"]
            temp = options[ans_index]
            options[ans_index] = options[fixed_index]
            options[fixed_index] = temp
            each["options"] = options
            each["answer_index"] = fixed_index
            each["answer"] = choices[fixed_index]
        res.append(each)
        # print("fixed", each)
        # input("enter")
    return res


def get_initial_prompt(subject):
    ins_file_name = f"ins_{str(args.prompt_type)}.txt"
    ins_file_path = os.path.join("prompt_lib", ins_file_name)
    prompt = ""
    with open(ins_file_path, "r") as fi:
        for line in fi.readlines():
            prompt += line + "\n"
    prompt = prompt.replace("{$}", subject)
    prompt += "\n\n"
    return prompt


def gen_prompt(train_df, subject, k=-1):
    prompt = get_initial_prompt(format_subject(subject))

    if k == -1:
        k = len(train_df)
    for i in range(k):
        p, options = format_example(train_df, i)
        prompt += p
    return prompt


def check_exist(res, q_id):
    for each in res:
        if q_id == each["question_id"]:
            if "pred" in each:
                print("exist, skip it")
                return True
            else:
                print("no result in exist result error")
                return False
        else:
            continue
    return False


def load_exist_result(res):
    corr_count, wrong_count = 0.0, 0.0
    for each in res:
        if "pred_score" in each:
            if each["pred_score"] == "True":
                corr_count += 1
            else:
                wrong_count += 1
    return corr_count, wrong_count


def load_model():
    # model, tokenizer = None, None
    if args.scoring_method == "CoT":
        llm = LLM(model=args.model, gpu_memory_utilization=0.7)
        sampling_params = SamplingParams(temperature=0, max_tokens=256,
                                         stop=["Question:"])
        tokenizer = transformers.AutoTokenizer.from_pretrained(args.model)
        return (llm, sampling_params), tokenizer
    if "llama-2" in args.model.lower():
        model = transformers.AutoModelForCausalLM.from_pretrained(
            args.model,
            device_map="auto", torch_dtype=torch.bfloat16)
        tokenizer = transformers.LlamaTokenizer.from_pretrained(
            args.model,
            model_max_length=2048,
            padding_side="right",
            use_fast=False,
        )
        tokenizer.add_special_tokens(
            {
                "eos_token": DEFAULT_EOS_TOKEN,
                "bos_token": DEFAULT_BOS_TOKEN,
                "unk_token": DEFAULT_UNK_TOKEN,
            }
        )
    elif "gemma" in args.model.lower() or "mistral" in args.model.lower() \
            or "yi-6b" in args.model.lower() or "llama-3" in args.model.lower():
        tokenizer = AutoTokenizer.from_pretrained(args.model,
                                                  model_max_length=2048,
                                                  padding_side="right",
                                                  use_fast=False)
        model = AutoModelForCausalLM.from_pretrained(args.model, device_map="auto", torch_dtype=torch.bfloat16)
        print("length of {} tokenizer".format(args.model), len(tokenizer))
    else:
        model, tokenizer = None, None
    return model, tokenizer


def batch_inference(llm, sampling_params, inference_batch):
    start = time.time()
    outputs = llm.generate(inference_batch, sampling_params)
    logging.info(str(len(inference_batch)) + "size batch costing time: " + str(time.time() - start))
    response_batch = []
    pred_batch = []
    for output in outputs:
        generated_text = output.outputs[0].text
        response_batch.append(generated_text)
        pred = extract_answer(generated_text)
        pred_batch.append(pred)
    return pred_batch, response_batch


def format_cot_example(example, including_answer=True):
    prompt = "Question:\n"
    question = example["question"]
    options = example["options"]
    prompt += question + "\n"
    prompt += "Options:\n"
    for i, opt in enumerate(options):
        prompt += "{}. {}\n".format(choices[i], opt)
    prompt += "\n\nAnswer:\n"
    prompt += example["cot_content"] + "\n\n"
    return prompt


def select_by_category(df, subject):
    res = []
    for each in df:
        if each["category"] == subject:
            res.append(each)
    return res


def generate_cot_prompt(dev_df, curr):
    prompt = ""
    with open(f"cot_ins_{str(args.prompt_type)}.txt", "r") as fi:
        for line in fi.readlines():
            prompt += line
    subject = curr["category"]
    dev_df = select_by_category(dev_df, subject)
    prompt = prompt.replace("{$}", subject) + "\n"
    for example in dev_df:
        prompt += format_cot_example(example, including_answer=True)
    prompt += format_cot_example(curr, including_answer=False)
    return prompt


@torch.no_grad()
def eval_cot(subject, model, tokenizer, dev_df, test_df, output_path, exists_result=None):
    llm, sampling_params = model
    if not exists_result:
        res = []
    else:
        res = exists_result
    # correct_count, wrong_count = load_exist_result(res)
    print("load exists result length", len(res))
    global choices
    logging.info("evaluating " + subject)
    batch_size = 8
    inference_batches = []
    label_batches = []
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
        prompt, label = generate_cot_prompt(dev_df, curr)
        inference_batches.append(prompt)
        # label_batches.append(label)
        in_batch_index.append(i)

    i = 0
    while i < len(test_df):
        if i + batch_size < len(test_df):
            end_index = i + batch_size
        else:
            end_index = len(test_df)
        curr_batch = inference_batches[i: end_index]
        # curr_labels = label_batches[i: end_index]
        pred_batch, response_batch = batch_inference(llm, sampling_params, curr_batch)
        index_list = in_batch_index[i: end_index]
        for j, index in enumerate(index_list):
            curr = test_df[index]
            curr["pred"] = pred_batch[j]
            curr["generated_text"] = response_batch[j]
            res.append(curr)
        save_res(res, output_path)
    accu, corr, wrong = save_res(res, output_path)
    return accu, corr, wrong


def save_res(res, output_path):
    accu, corr, wrong = 0.0, 0.0, 0.0
    with open(output_path, "w") as fo:
        fo.write(json.dumps(res))
    for each in res:
        if each["pred"] is None:
            logging.info("answer extract failed\n" + each["generated_text"])
            continue
        if each["pred"] == each["answer"]:
            corr += 1
        else:
            wrong += 1
    accu = corr / (corr + wrong)
    return accu, corr, wrong


def extract_answer(text):
    pattern = r"answer is \(?([ABCDEFGHIJ])\)?"
    match = re.search(pattern, text)
    if match:
        return match.group(1)
    else:
        return None


def gen_cot_prompt(subject, k, tokenizer):
    subject = format_subject(subject)
    if subject not in cot_lib:
        print("subject not in cot_lib", subject)
        return None
    k = min(k, len(cot_lib[subject]))
    if args.prompt_type == 1:
        prompt = ""
    elif args.prompt_type == 2:
        prompt = "You are an expert in {}. Below is a series of example questions \
        (with answers) about {} for demonstration. You will be given a question at \
        the end, after the examples, for you to answer.\n\n".format(format_subject(subject),
                                                                    format_subject(subject))
    else:
        prompt = "The following are multiple choice questions (with answers) about {}.\n\n" \
            .format(format_subject(subject))
    if k == -1:
        k = 5
    temp = ""
    for i in range(k):
        curr_example = cot_lib[subject][i]
        option_num = len(curr_example["options"])
        p = "Question: " + curr_example["question"] + "\nOptions: \n"
        for j in range(option_num):
            p += "{}. {}\n".format(choices[j], curr_example["options"][j])
        cot_content = curr_example["cot_content"].replace("A: Let's think step by step.",
                                                          "Let's think step by step.")
        p += "Answer: " + cot_content + "\n"
        prompt += p
        # inputs = tokenizer.encode(prompt, return_tensors="pt")
        # logging.info("gen prompt input length[0]" + str(len(inputs[0])))
        # if len(inputs[0]) > 1600:
        #     prompt = temp
        #     logging.info("use less examples due to length limit " + str(i))
        #     break
        # temp = prompt
    return prompt


@torch.no_grad()
def eval(subject, model, tokenizer, dev_df, test_df, output_path, exists_result=None):
    if not exists_result:
        res = []
    else:
        res = exists_result
    correct_count, wrong_count = load_exist_result(res)
    print("load exists result length", len(res))
    global choices
    if args.use_rare_symbol:
        greek_upper_unicode_start = 0x391
        greek_letters = [chr(greek_upper_unicode_start + i) for i in range(17)]
        choices = greek_letters

    for i in tqdm(range(len(test_df))):
        k = args.ntrain
        options_num = len(test_df[i]["options"])
        if options_num != 10 and options_num != 4:
            print("options_num", options_num)
        prompt_end, options = format_example(test_df, i, include_answer=False)
        if check_exist(res, test_df[i]["q_id"]):
            continue
        train_prompt = gen_prompt(dev_df, subject, k)
        prompt = train_prompt + prompt_end
        if i == 0:
            print("train_prompt", train_prompt)
            # logging.info("prompt:\n" + prompt)

        label = test_df[i]["answer"]

        if args.scoring_method == "hybrid_scoring":
            prompt_input_ids = tokenizer.encode(prompt, return_tensors="pt")
            while prompt_input_ids.shape[-1] > 2000:
                k -= 1
                train_prompt = gen_prompt(dev_df, subject, k)
                prompt = train_prompt + prompt_end
                prompt_input_ids = tokenizer.encode(prompt, return_tensors="pt")
            log_likelihoods = []
            for opt in options:
                full_text = prompt + opt
                input_ids = tokenizer.encode(full_text, return_tensors="pt").cuda()
                labels = torch.full(input_ids.shape, -100).cuda()
                start_target = len(prompt_input_ids)
                labels[0, start_target:] = input_ids[0, start_target:]
                loss = model(input_ids, labels=labels).loss
                log_likelihoods.append(-loss.item())
            probs = torch.nn.functional.softmax(torch.tensor(log_likelihoods), dim=0).detach().cpu().numpy()
            pred = choices[np.argmax(probs)]

        elif args.scoring_method == "symbol_scoring":
            input_ids = tokenizer(prompt, return_tensors="pt").input_ids.cuda()
            while input_ids.shape[-1] > 2000:
                k -= 1
                train_prompt = gen_prompt(dev_df, subject, k)
                prompt = train_prompt + prompt_end
                input_ids = tokenizer(prompt, return_tensors="pt").input_ids.cuda()
            logits = model(
                input_ids=input_ids  # decoder_input_ids=decoder_input_ids
            ).logits

            chars = "".join(choices)
            probs = (torch.nn.functional.softmax(torch.tensor(
                        [logits[0, -1, tokenizer(chars[i]).input_ids[-1]] for i in range(options_num)]
                    ).to(torch.float32), dim=0,).detach().cpu().numpy())
            # print(probs)
            letters = [chr(i) for i in range(ord('A'), ord('Z') + 1)]

            index_letter_dict = {i: letters[i] for i in range(options_num)}
            pred = index_letter_dict[np.argmax(probs)]
        else:
            print("unsupported scoring method")
            pred = False
            probs = []

        curr = test_df[i]
        curr["pred"] = pred
        if pred == label:
            curr["pred_score"] = "True"
            correct_count += 1
        else:
            curr["pred_score"] = "False"
            wrong_count += 1
        curr["probs"] = probs.tolist()
        res.append(curr)
        with open(output_path, "w") as fo:
            fo.write(json.dumps(res))

    acc = correct_count / (correct_count + wrong_count)
    if os.path.exists(summary_path):
        with open(summary_path, "a") as fo:
            fo.write("Average accuracy {:.4f} - {}".format(acc, subject) + "\n")
    else:
        with open(summary_path, "w") as fo:
            fo.write("Average accuracy {:.4f} - {}".format(acc, subject) + "\n")
    return acc, correct_count, wrong_count


def divide_df(all_df):
    start_index = args.examples_start_index
    example_num = args.ntrain
    dev_df = all_df[start_index: start_index + example_num]
    test_df = all_df[: start_index] + all_df[start_index + example_num:]
    return dev_df, test_df


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


def main():
    model, tokenizer = load_model()
    if args.scoring_method != "CoT":
        print("model.eval()")
        model.eval()
    if not os.path.exists(save_result_dir):
        os.makedirs(save_result_dir)

    if "ori_mmlu" in args.data_dir:
        dataset = "ori_mmlu"
    else:
        dataset = "mmlu_pro"
    with open(os.path.join(args.data_dir, dataset + "_test.json"), "r") as fi:
        test_df = json.load(fi)
    with open(os.path.join(args.data_dir, dataset + "_dev.json"), "r") as fi:
        dev_df = json.load(fi)
    test_df = preprocess(test_df)
    dev_df = preprocess(dev_df)
    all_subjects = []
    for each in test_df:
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
    for subject in selected_subjects:
        if subject not in sta_dict:
            sta_dict[subject] = {"corr": 0.0, "wrong": 0.0, "accu": 0.0}
        test_df = select_by_category(test_df, subject)
        dev_df = select_by_category(dev_df, subject)
        output_path = os.path.join(save_result_dir, "{}".format(subject))
        if os.path.exists(output_path):
            with open(output_path, "r") as fi:
                exists_result = json.load(fi)
        else:
            exists_result = []
        if args.scoring_method == "CoT":
            acc, corr_count, wrong_count = eval_cot(subject, model, tokenizer, dev_df,
                                                    test_df, output_path, exists_result)
        else:
            acc, corr_count, wrong_count = eval(subject, model, tokenizer, dev_df,
                                                test_df, output_path, exists_result)
        sta_dict[subject]["corr"] = corr_count
        sta_dict[subject]["wrong"] = wrong_count
        sta_dict[subject]["accu"] = acc
    total_corr, total_wrong = 0.0, 0.0
    for k, v in sta_dict.items():
        total_corr += v["corr"]
        total_wrong += v["wrong"]
    total_accu = total_corr / (total_corr + total_wrong)
    sta_dict["total"] = {"corr": total_corr, "wrong": total_wrong, "accu": total_accu}

    with open(os.path.join(summary_path), 'a') as f:
        f.write("\n------category level sta------\n")
        for subject in selected_subjects:
            f.write("Average accuracy {:.4f} - {}\n".format(sta_dict[subject]["accu"], subject))
        f.write("\n------average acc sta------\n")
        weighted_acc = total_accu
        f.write("Average accuracy: {:.4f}\n".format(weighted_acc))
    with open(global_record_file, 'a', newline='') as file:
        writer = csv.writer(file)
        record = args_generate_path(args) + [time_str, weighted_acc]
        writer.writerow(record)


def args_generate_path(input_args):
    scoring_method = input_args.scoring_method
    # if args.cot_type != "-1":
    #     scoring_method = args.cot_type
    model_name = input_args.model.split("/")[-1]
    if "ori_mmlu" in input_args.data_dir:
        dataset_name = "mmlu"
    else:
        dataset_name = "mmlu_pro"
    examples_start_index = f"es_{str(input_args.examples_start_index)}"
    prompt_type = f"prompt_{str(input_args.prompt_type)}"
    prompt_format = f"format_{str(input_args.prompt_format)}"
    subjects = args.selected_subjects.replace(",", "-").replace(" ", "_")
    return [scoring_method, model_name, dataset_name, examples_start_index, prompt_type,
            prompt_format, subjects]


def read_csv_file(file_path):
    with open(file_path, mode='r', encoding='utf-8') as file:
        csv_reader = csv.reader(file)
        data = list(csv_reader)
        if str(data[0][0]) == "0" and str(data[0][1]) == "1" and str(data[0][2]) == "2":
            data = data[1:]
    return data


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ntrain", "-k", type=int, default=5)
    parser.add_argument("--examples_start_index", "-esi", type=int, default=0)
    parser.add_argument("--prompt_type", "-p", type=int, default=0)
    parser.add_argument("--prompt_format", "-pf", type=int, default=0)
    parser.add_argument("--selected_subjects", "-sub", type=str, default="all")
    # parser.add_argument("--cot_type", "-c", type=str, default="-1")
    parser.add_argument("--ngpu", "-g", type=int, default=1)
    parser.add_argument("--data_dir", "-d", type=str, default="data")
    parser.add_argument("--save_dir", "-s", type=str, default="results")
    parser.add_argument("--options_num", "-o", type=int, default=4)
    parser.add_argument("--use_rare_symbol", "-r", type=lambda x: bool(strtobool(x)), default=False)
    parser.add_argument("--fixed_question_answer", "-q", type=int, default=-1)
    parser.add_argument("--scoring_method", "-sm", type=str, default="symbol_scoring")
    parser.add_argument(
        "--model",
        "-m",
        type=str,
        default="/ML-A100/team/mm/zhangge/Llama-2-7b-hf",
    )
    global_record_file = "../result_record/eval_record_collection_0513.csv"
    os.makedirs("../result_record", exist_ok=True)
    args = parser.parse_args()
    # cot_lib = load_cot_lib()
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

'''
model="/ML-A100/team/mm/zhangge/Llama-2-7b-hf"
model="google/gemma-7b"
model="/ML-A100/team/mm/zhangge/Llama-2-13b-hf"
model="/mnt/tjena/shared/Meta-Llama-3-8B"
model="/ML-A100/team/mm/zhangge/Llama-2-7b-chat-hf"
model="01-ai/Yi-6B"
model="mistralai/Mixtral-8x7B-v0.1"
meta-llama
Llama-2-7b-hf

variance
ranking big difference
'''
