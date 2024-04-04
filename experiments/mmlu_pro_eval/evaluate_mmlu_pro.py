import warnings
warnings.filterwarnings("ignore")
import csv
import argparse
import os
import torch
import numpy as np
import pandas as pd
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
from transformers import AutoModelForCausalLM
from categories import subcategories, categories
import transformers
import time
from transformers import GenerationConfig
from tqdm import tqdm
from distutils.util import strtobool


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


def smart_tokenizer_and_embedding_resize(
        special_tokens_dict,
        tokenizer,
        model,
):
    """Resize tokenizer and embedding.

    Note: This is the unoptimized version that may make your embedding size not be divisible by 64.
    """
    num_new_tokens = tokenizer.add_special_tokens(special_tokens_dict)
    model.resize_token_embeddings(len(tokenizer))

    if num_new_tokens > 0:
        input_embeddings = model.get_input_embeddings().weight.data
        # output_embeddings = model.get_output_embeddings().weight.data

        input_embeddings_avg = input_embeddings[:-num_new_tokens].mean(dim=0, keepdim=True)
        # output_embeddings_avg = output_embeddings[:-num_new_tokens].mean(dim=0, keepdim=True)

        input_embeddings[-num_new_tokens:] = input_embeddings_avg
        # output_embeddings[-num_new_tokens:] = output_embeddings_avg


def read_csv_file(file_path):
    with open(file_path, mode='r', encoding='utf-8') as file:
        csv_reader = csv.reader(file)
        data = list(csv_reader)
        if str(data[0][0]) == "0" and str(data[0][1]) == "1" and str(data[0][2]) == "2":
            data = data[1:]
    return data


def write_2dlist_to_csv(data, file_name):
    with open(file_name, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerows(data)


def fix_answer(all_df, fixed_answer_index):
    column_names = all_df.columns.tolist()
    all_data_list = all_df.to_numpy().tolist()
    for i, row in enumerate(all_data_list):
        ans = row[5]
        ans_index = "ABCDEFGHIJKLMNOPQRSTUVWXYZ".index(ans)
        if ans_index != fixed_answer_index:
            all_data_list[i][-2] = choices[fixed_answer_index]
            temp = row[fixed_answer_index + 1]
            all_data_list[i][fixed_answer_index + 1] = row[ans_index + 1]
            all_data_list[i][ans_index + 1] = temp
    all_df = pd.DataFrame(all_data_list, columns=column_names)
    return all_df


def format_subject(subject):
    return subject.replace(".csv", "")


def format_example(df, idx, include_answer=True):
    prompt = str(df.iloc[idx, 0])
    k = df.shape[1] - 3
    options = []
    for j in range(k):
        prompt += "\n{}. {}".format(choices[j], str(df.iloc[idx, j + 1]))
        options.append(str(df.iloc[idx, j + 1]))
    prompt += "\nAnswer:"
    if include_answer:
        ori_ans = df.iloc[idx, k + 1]
        ans_index = "ABCDEFGHIJKLMNOPQRSTUVWXYZ".index(ori_ans)
        prompt += " {}\n\n".format(options[ans_index])

    return prompt, options


def gen_prompt(train_df, subject, k=-1):
    if subject and subject != "":
        prompt = "The following are multiple choice questions (with answers) about {}.\n\n".format(
            format_subject(subject)
        )
    else:
        prompt = ""
    if k == -1:
        k = train_df.shape[0]
    for i in range(k):
        p, options = format_example(train_df, i)
        prompt += p
    return prompt


def load_exists_result(exists_result):
    cors = []
    all_probs = []
    for each in exists_result:
        if len(each) != 4 + 2 * args.options_num:
            print("invalid exists_result row length", each)
            curr_cor = False
            curr_probs = [0 for _ in range(args.options_num)]
        else:
            curr_cor = str(each[len(each) - args.options_num - 1]) == "True"
            curr_probs = each[-args.options_num:]
        # print("curr_cor", curr_cor)
        # print("curr_probs", curr_probs)
        cors.append(curr_cor)
        all_probs.append(curr_probs)
    return cors, all_probs


def check_exist(exists_result, question_option_str, index):
    if index < len(exists_result):
        return True
    return False
    # for each in exists_result:
    #     curr = ""
    #     for i in range(args.options_num + 1):
    #         curr += str(each[i]) + "\n"
    #     if curr == question_option_str and index < len(exists_result):
    #         return True
    # return False


@torch.no_grad()
def eval(args, subject, model, tokenizer, dev_df, test_df, exists_result=None):
    if not exists_result:
        exists_result = []
    cors, all_probs = load_exists_result(exists_result)
    print("load exists result length", len(exists_result), len(cors))
    global choices
    if args.use_rare_symbol:
        greek_upper_unicode_start = 0x391
        # 创建一个列表，包含1-20对应的大写希腊字母
        greek_letters = [chr(greek_upper_unicode_start + i) for i in range(17)]
        choices = greek_letters
    answers = choices[: test_df.shape[1] - 2]

    for i in tqdm(range(test_df.shape[0])):
        # get prompt and make sure it fits
        k = args.ntrain
        prompt_end, options = format_example(test_df, i, include_answer=False)
        question_option_str = ""
        for index in range(args.options_num + 1):
            question_option_str += str(test_df.iloc[i, index]) + "\n"
        if check_exist(exists_result, question_option_str, i):
            continue
        # print("not exist", question_option_str)
        train_prompt = gen_prompt(dev_df, subject, k)
        prompt = train_prompt + prompt_end

        input_ids = tokenizer(prompt, return_tensors="pt").input_ids.cuda()

        while input_ids.shape[-1] > 2048:
            k -= 1
            train_prompt = gen_prompt(dev_df, subject, k)
            prompt = train_prompt + prompt_end
            input_ids = tokenizer(prompt, return_tensors="pt").input_ids.cuda()

        label = test_df.iloc[i, test_df.shape[1] - 2]

        logits = model(
            input_ids=input_ids  # decoder_input_ids=decoder_input_ids
        ).logits

        chars = "".join(choices)
        probs = (
            torch.nn.functional.softmax(
                torch.tensor(
                    [
                        logits[0, -1, tokenizer(chars[i]).input_ids[-1]] for i in range(args.options_num)
                    ]
                ),
                dim=0,
            )
            .detach()
            .cpu()
            .numpy()
        )
        # print(probs)
        letters = [chr(i) for i in range(ord('A'), ord('Z') + 1)]

        # 使用字典推导式构建特定长度的字典
        index_letter_dict = {i: letters[i] for i in range(args.options_num)}
        pred = index_letter_dict[np.argmax(probs)]

        cor = pred == label
        cors.append(cor)
        all_probs.append(probs)

    acc = np.mean(cors)
    cors = np.array(cors)

    all_probs = np.array(all_probs)
    # global save_result_dir
    if os.path.exists(save_result_path):
        with open(save_result_path, "a") as fo:
            fo.write("Average accuracy {:.4f} - {}".format(acc, subject) + "\n")
    else:
        with open(save_result_path, "w") as fo:
            fo.write("Average accuracy {:.4f} - {}".format(acc, subject) + "\n")
    return cors, acc, all_probs


def hybrid_eval(args, subject, model, tokenizer, dev_df, test_df, exists_result=None):
    if not exists_result:
        exists_result = []
    cors, all_probs = load_exists_result(exists_result)
    global choices
    if args.use_rare_symbol:
        greek_upper_unicode_start = 0x391

        # 创建一个列表，包含1-20对应的大写希腊字母
        greek_letters = [chr(greek_upper_unicode_start + i) for i in range(17)]
        choices = greek_letters
    answers = choices[: test_df.shape[1] - 2]

    for i in tqdm(range(test_df.shape[0])):
        # get prompt and make sure it fits
        k = args.ntrain
        prompt_end, options = format_example(test_df, i, include_answer=False)
        question_option_str = ""
        for index in range(args.options_num + 1):
            question_option_str += str(test_df.iloc[i, index]) + "\n"
        if check_exist(exists_result, question_option_str, i):
            continue
        train_prompt = gen_prompt(dev_df, subject, k)
        prompt = train_prompt + prompt_end

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

        label = test_df.iloc[i, test_df.shape[1] - 2]
        cor = pred == label
        cors.append(cor)
        all_probs.append(probs)

    acc = np.mean(cors)
    cors = np.array(cors)

    all_probs = np.array(all_probs)

    if os.path.exists(save_result_path):
        with open(save_result_path, "a") as fo:
            fo.write("Average accuracy {:.4f} - {}".format(acc, subject) + "\n")
    else:
        with open(save_result_path, "w") as fo:
            fo.write("Average accuracy {:.4f} - {}".format(acc, subject) + "\n")
    return cors, acc, all_probs


def main(args):
    # model, tokenizer = None, None
    if "llama" in args.model.lower():
        model = transformers.AutoModelForCausalLM.from_pretrained(
            args.model,
            device_map="auto",
        )
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
            or "yi-6b" in args.model.lower():
        tokenizer = AutoTokenizer.from_pretrained(args.model,
                                                  model_max_length=2048,
                                                  padding_side="right",
                                                  use_fast=False)
        model = AutoModelForCausalLM.from_pretrained(args.model, device_map="auto")
        print("length of {} tokenizer".format(args.model), len(tokenizer))
    else:
        model, tokenizer = None, None
    print("model.eval()")
    model.eval()

    subjects = sorted(
        [
            f
            for f in os.listdir(args.data_dir)
            if ".csv" in f
        ]
    )

    if not os.path.exists(args.save_dir):
        os.makedirs(args.save_dir)
    if not os.path.exists(save_result_dir):
        os.makedirs(save_result_dir)

    all_cors = []

    subcat_cors = {}

    for subcat in subcategories.values():
        subcat_cors[subcat] = []

    cat_cors = {cat: [] for cat in categories}

    for subject in subjects:
        if os.path.exists(os.path.join(save_result_dir, "{}".format(subject))):
            exists_result = read_csv_file(os.path.join(save_result_dir, "{}".format(subject)))
        else:
            exists_result = []
        all_data = read_csv_file(os.path.join(args.data_dir, subject))
        all_df = pd.DataFrame(all_data)
        # print("all_df length", len(all_df.values.tolist()))
        dev_df = all_df[: args.ntrain]
        test_df = all_df[args.ntrain:]
        # print("test_df length", len(test_df.values.tolist()))
        if args.fixed_answer != -1:
            dev_df = fix_answer(dev_df, args.fixed_answer)
            test_df = fix_answer(test_df, args.fixed_answer)
        elif args.fixed_example_answer != -1:
            dev_df = fix_answer(dev_df, args.fixed_example_answer)
        elif args.fixed_question_answer != -1:
            test_df = fix_answer(test_df, args.fixed_question_answer)
        if args.scoring_method == "hybrid_scoring":
            cors, acc, probs = hybrid_eval(args, subject, model, tokenizer, dev_df, test_df, exists_result)
        else:
            cors, acc, probs = eval(args, subject, model, tokenizer, dev_df, test_df, exists_result)
        subcat = subcategories[subject]
        subcat_cors[subcat].append(cors)
        for key in categories.keys():
            if subcat in categories[key]:
                cat_cors[key].append(cors)
        all_cors.append(cors)

        test_df["{}_correct".format(args.model)] = cors
        for j in range(probs.shape[1]):
            choice = choices[j]
            test_df["{}_choice_{}_probs".format(args.model, choice)] = probs[:, j]
        test_data = test_df.to_numpy().tolist()
        write_2dlist_to_csv(test_data, os.path.join(save_result_dir, "{}".format(subject)))

    with open(os.path.join(save_result_path), 'a') as f:
        f.write("\n------category level sta------\n")
        for cat in cat_cors:
            if not cat_cors[cat]:
                continue
            cat_acc = np.mean(np.concatenate(cat_cors[cat]))
            f.write("Average accuracy {:.4f} - {}\n".format(cat_acc, cat))

        f.write("\n------average acc sta------\n")
        weighted_acc = np.mean(np.concatenate(all_cors))
        f.write("Average accuracy: {:.4f}\n".format(weighted_acc))


def args_generate_path(input_args):
    scoring_method = input_args.scoring_method
    model_name = input_args.model.split("/")[-1]
    if "ori" in input_args.data_dir:
        dataset_name = "mmlu"
    else:
        dataset_name = "mmlu_pro"
    if input_args.options_num > 4:
        dataset_name += f"_exp_{str(input_args.options_num)}"
    if input_args.fixed_question_answer == -1 and not input_args.use_rare_symbol:
        eval_method = "ori_eval"
    elif input_args.fixed_question_answer == -1:
        eval_method = "rare_symbol"
    elif input_args.fixed_question_answer != -1:
        fix_map = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        eval_method = f"fix_{fix_map[input_args.fixed_question_answer]}"
    else:
        eval_method = "ori_eval"
    res = f"{scoring_method}/{model_name}/{dataset_name}/{eval_method}"
    return res


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ntrain", "-k", type=int, default=5)
    parser.add_argument("--ngpu", "-g", type=int, default=1)
    parser.add_argument("--data_dir", "-d", type=str, default="data")
    parser.add_argument("--save_dir", "-s", type=str, default="results")
    parser.add_argument("--options_num", "-o", type=int, default=4)
    parser.add_argument("--use_rare_symbol", "-r", type=lambda x: bool(strtobool(x)), default=False)
    parser.add_argument("--fixed_answer", "-f", type=int, default=-1)
    parser.add_argument("--fixed_example_answer", "-e", type=int, default=-1)
    parser.add_argument("--fixed_question_answer", "-q", type=int, default=-1)
    parser.add_argument("--scoring_method", "-sm", type=str, default="symbol_scoring")
    parser.add_argument(
        "--model",
        "-m",
        type=str,
        default="/ML-A100/team/mm/zhangge/Llama-2-7b-hf",
    )
    args = parser.parse_args()
    save_result_dir = os.path.join(
        args.save_dir, args_generate_path(args)
    )
    file_prefix = args_generate_path(args).replace("/", "-")
    timestamp = time.time()
    time_str = time.strftime('%m-%d_%H-%M', time.localtime(timestamp))
    file_name = f"{file_prefix}_{time_str}_summary.txt"
    save_result_path = os.path.join(args.save_dir, file_name)
    main(args)
