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
from transformers import GenerationConfig
from tqdm import tqdm
from distutils.util import strtobool
import logging
import sys


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
    prompt = ""
    if args.prompt_type == 1:
        prompt += "Question:"
    prompt += str(df[idx]["question"])
    if args.prompt_type == 1:
        prompt += "\nOptions:"
    options = df[idx]["options"]
    for j in range(len(options)):
        prompt += "\n{}. {}".format(choices[j], options[j])
    prompt += "\nAnswer:"
    if include_answer:
        ans_index = df[idx]["answer_index"]
        if args.scoring_method == "symbol_scoring":
            prompt += " {}\n\n".format(choices[ans_index])
        elif args.scoring_method == "hybrid_scoring":
            prompt += " {}\n\n".format(options[ans_index])
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


def gen_prompt(train_df, subject, k=-1):
    if subject and subject != "":
        if args.prompt_type == 1:
            prompt = ""
        elif args.prompt_type == 2:
            prompt = "You are an expert in {}. Below is a series of example questions \
            (with answers) about {} for demonstration. You will be given a question at \
            the end, after the examples, for you to answer.\n\n".format(format_subject(subject),
                                                                        format_subject(subject))
        else:
            prompt = "The following are multiple choice questions (with answers) about {}.\n\n"\
                .format(format_subject(subject))
    else:
        prompt = ""
    if k == -1:
        k = len(train_df)
    for i in range(k):
        p, options = format_example(train_df, i)
        prompt += p
    return prompt


def check_exist(res, q_id):
    for each in res:
        if q_id == each["q_id"]:
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


@torch.no_grad()
def eval_cot(subject, model, tokenizer, dev_df, test_df, output_path, exists_result=None):
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
        curr = test_df[i]
        prompt_end = "Question: " + curr["question"] + "\nOptions: \n"
        for j in range(options_num):
            prompt_end += "{}. {}\n".format(choices[j], curr["options"][j])
        prompt_end += "Answer: Let's think step by step."
        if check_exist(res, test_df[i]["q_id"]):
            continue
        train_prompt = gen_cot_prompt(subject, k)
        prompt = train_prompt + prompt_end
        if i == 0:
            print("prompt", prompt)
            logging.info("prompt:\n" + prompt)
        label = test_df[i]["answer"]
        inputs = tokenizer(prompt, return_tensors="pt")
        output = model.generate(**inputs, max_length=512, num_return_sequences=1)
        answer = tokenizer.decode(output[0], skip_special_tokens=True)
        pred = extract_answer(answer)
        if not pred:
            temp = choices[: options_num]
            random.shuffle(temp)
            pred = temp[0]
            logging.info("answer extract failed", answer, "pred random select", pred)

            curr = test_df[i]
            curr["pred"] = pred
            if pred == label:
                curr["pred_score"] = "True"
                correct_count += 1
            else:
                curr["pred_score"] = "False"
                wrong_count += 1
            curr["full_text_answer"] = answer
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


def extract_answer(text):
    pattern = r"answer is \(?([ABCD])\)?"
    match = re.search(pattern, text)
    if match:
        return match.group(1)
    else:
        return None


def gen_cot_prompt(subject, k):
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
            logging.info("prompt:\n" + prompt)

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


def main():
    model, tokenizer = load_model()
    print("model.eval()")
    model.eval()

    subjects = sorted([f for f in os.listdir(args.data_dir) if ".json" in f])

    if not os.path.exists(save_result_dir):
        os.makedirs(save_result_dir)

    all_cors = []
    if "ori_mmlu" in args.data_dir:
        subcat_dict = ori_mmlu_subcategories
        cat_dict = ori_mmlu_categories
    else:
        subcat_dict = subcategories
        cat_dict = categories
    subcat_cors = {}
    for subcat in subcat_dict.values():
        subcat_cors[subcat] = []
    cat_cors = {cat: [] for cat in cat_dict}

    for subject in subjects:
        output_path = os.path.join(save_result_dir, "{}".format(subject))
        if os.path.exists(output_path):
            with open(output_path, "r") as fi:
                exists_result = json.load(fi)
        else:
            exists_result = []
        with open(os.path.join(args.data_dir, subject), "r") as fi:
            all_df = json.load(fi)
        dev_df, test_df = divide_df(all_df)
        print("dev_df", dev_df)
        logging.info(json.dumps(dev_df))
        if args.fixed_question_answer != -1:
            test_df = fix_answer(test_df, args.fixed_question_answer)
        if args.cot_type == "cot_1":
            acc, corr_count, wrong_count = eval_cot(subject, model, tokenizer, dev_df,
                                                    test_df, output_path, exists_result)
        else:
            acc, corr_count, wrong_count = eval(subject, model, tokenizer, dev_df,
                                                test_df, output_path, exists_result)
        subcat = subcat_dict[subject.replace(".json", "")]
        cors = [0 for _ in range(int(wrong_count))] + [1 for _ in range(int(corr_count))]
        subcat_cors[subcat].append(cors)
        for key in cat_dict.keys():
            if subcat in cat_dict[key]:
                cat_cors[key].append(cors)
        all_cors.append(cors)

    with open(os.path.join(summary_path), 'a') as f:
        f.write("\n------subcategory level sta------\n")
        keys = list(subcat_cors.keys())
        keys = sorted(keys)
        for subcat in keys:
            if not subcat_cors[subcat]:
                continue
            subcat_acc = np.mean(np.concatenate(subcat_cors[subcat]))
            f.write("Average accuracy {:.4f} - {}\n".format(subcat_acc, subcat))

        f.write("\n------category level sta------\n")
        for cat in cat_cors:
            if not cat_cors[cat]:
                continue
            cat_acc = np.mean(np.concatenate(cat_cors[cat]))
            f.write("Average accuracy {:.4f} - {}\n".format(cat_acc, cat))

        f.write("\n------average acc sta------\n")
        weighted_acc = np.mean(np.concatenate(all_cors))
        f.write("Average accuracy: {:.4f}\n".format(weighted_acc))
    with open(global_record_file, "a") as fi:
        record = file_prefix + "\t\t" + time_str + "\t\t" + str(weighted_acc) + "\n"
        fi.write(record)


def args_generate_path(input_args):
    scoring_method = input_args.scoring_method
    model_name = input_args.model.split("/")[-1]
    if "ori_mmlu" in input_args.data_dir:
        dataset_name = "mmlu"
    else:
        dataset_name = "mmlu_pro"
    if input_args.fixed_question_answer == -1 and not input_args.use_rare_symbol:
        eval_method = "ori_eval"
    elif input_args.fixed_question_answer == -1:
        eval_method = "rare_symbol"
    elif input_args.fixed_question_answer != -1:
        fix_map = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        eval_method = f"fix_{fix_map[input_args.fixed_question_answer]}"
    else:
        eval_method = "ori_eval"
    examples_start_index = f"es_{str(input_args.examples_start_index)}"
    prompt_type = f"prompt_{str(input_args.prompt_type)}"
    res = f"{scoring_method}/{model_name}/{dataset_name}/{eval_method}/{examples_start_index}/{prompt_type}"
    return res


def read_csv_file(file_path):
    with open(file_path, mode='r', encoding='utf-8') as file:
        csv_reader = csv.reader(file)
        data = list(csv_reader)
        if str(data[0][0]) == "0" and str(data[0][1]) == "1" and str(data[0][2]) == "2":
            data = data[1:]
    return data


def load_cot_lib():
    lib_data = {}
    seed = 123456
    random.seed(seed)
    if args.cot_type == "-1":
        return lib_data
    # else:
    elif args.cot_type == "cot_1":
        if "ori_mmlu" in args.data_dir:
            lib_path = "cot_lib_prompt/ori_mmlu-cot.csv"
            option_num = 4
        else:
            lib_path = "cot_lib_prompt/mmlu_pro-cot.csv"
            option_num = 10
        data = read_csv_file(lib_path)
        for each in data:
            each = each[1:]
            subject = each[0]
            question = each[1]
            options = each[2: 2 + option_num]
            answer_symbol = each[option_num + 2]
            answer_content = each[option_num + 3]
            cot_content = each[option_num + 4]
            if subject not in lib_data:
                lib_data[subject] = []
            if len(lib_data[subject]) >= 5:
                continue
            curr = {"question": question, "options": options, "answer_content": answer_content,
                    "answer_symbol": answer_symbol, "cot_content": cot_content}
            lib_data[subject].append(curr)
    return lib_data


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ntrain", "-k", type=int, default=5)
    parser.add_argument("--examples_start_index", "-esi", type=int, default=0)
    parser.add_argument("--prompt_type", "-p", type=int, default=0)
    parser.add_argument("--cot_type", "-c", type=str, default="-1")
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
        default="meta-llama/Llama-2-7b-hf",
    )
    global_record_file = "../result_record/eval_record_collection.txt"
    args = parser.parse_args()
    cot_lib = load_cot_lib()
    save_result_dir = os.path.join(
        args.save_dir, args_generate_path(args)
    )
    file_prefix = args_generate_path(args).replace("/", "-")
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
model="meta-llama/Llama-2-7b-hf"
model="google/gemma-7b"
model="meta-llama/Llama-2-13b-hf"
model="/mnt/tjena/shared/Meta-Llama-3-8B"
model="meta-llama/Llama-2-7b-chat-hf"
model="01-ai/Yi-6B"
model="mistralai/Mixtral-8x7B-v0.1"


variance
ranking big difference
'''

