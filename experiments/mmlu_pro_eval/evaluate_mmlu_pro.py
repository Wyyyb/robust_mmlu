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


def fix_answer(all_df, fixed_answer_index):
    column_names = all_df.columns.tolist()
    all_data_list = all_df.to_numpy().tolist()
    for i, row in enumerate(all_data_list):
        ans = row[5]
        ans_index = "ABCDEFGHIJKLMNOPQRSTUVWXYZ".index(ans)
        if ans_index != fixed_answer_index:
            all_data_list[i][-1] = choices[fixed_answer_index]
            temp = row[fixed_answer_index + 1]
            all_data_list[i][fixed_answer_index + 1] = row[ans_index + 1]
            all_data_list[i][ans_index + 1] = temp
    all_df = pd.DataFrame(all_data_list, columns=column_names)
    return all_df


def format_subject(subject):
    return subject.replace(".csv", "")


def format_example(df, idx, include_answer=True):
    prompt = df.iloc[idx, 0]
    k = df.shape[1] - 3
    for j in range(k):
        prompt += "\n{}. {}".format(choices[j], df.iloc[idx, j + 1])
    prompt += "\nAnswer:"
    if include_answer:
        ori_ans = df.iloc[idx, k + 1]
        ans_index = "ABCDEFGHIJKLMNOPQRSTUVWXYZ".index(ori_ans)
        prompt += " {}\n\n".format(choices[ans_index])
    print("prompt", prompt)
    return prompt


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
        prompt += format_example(train_df, i)
    return prompt


@torch.no_grad()
def eval(args, subject, model, tokenizer, dev_df, test_df):
    generation_config = GenerationConfig(
        do_sample=False
    )

    cors = []
    all_probs = []
    global choices
    if args.use_rare_symbol:
        greek_upper_unicode_start = 0x391

        # 创建一个列表，包含1-20对应的大写希腊字母
        greek_letters = [chr(greek_upper_unicode_start + i) for i in range(17)]
        choices = greek_letters
    answers = choices[: test_df.shape[1] - 2]

    for i in range(test_df.shape[0]):
        # get prompt and make sure it fits
        k = args.ntrain
        prompt_end = format_example(test_df, i, include_answer=False)
        train_prompt = gen_prompt(dev_df, subject, k)
        prompt = train_prompt + prompt_end

        input_ids = tokenizer(prompt, return_tensors="pt").input_ids.cuda()

        while input_ids.shape[-1] > 2048:
            k -= 1
            train_prompt = gen_prompt(dev_df, subject, k)
            prompt = train_prompt + prompt_end
            input_ids = tokenizer(prompt, return_tensors="pt").input_ids.cuda()

        label = test_df.iloc[i, test_df.shape[1] - 1]

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
    print("Average accuracy {:.3f} - {}".format(acc, subject))

    return cors, acc, all_probs


def main(args):
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
    elif "gemma" in args.model.lower() or "mistral" in args.model.lower():
        tokenizer = AutoTokenizer.from_pretrained(args.model,
                                                  model_max_length=2048,
                                                  padding_side="right",
                                                  use_fast=False,)
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
    if not os.path.exists(os.path.join(args.save_dir, "results_{}".format(args.model))):
        os.makedirs(os.path.join(args.save_dir, "results_{}".format(args.model)))
    save_result_dir = os.path.join(args.save_dir, "results_{}".format(args.model))

    all_cors = []

    subcat_cors = {}

    for subcat in subcategories.values():
        subcat_cors[subcat] = []

    # 现在 subcat_cors 字典包含了所有子类别作为键，每个键对应的值都是一个空列表
    cat_cors = {cat: [] for cat in categories}

    for subject in subjects:
        all_df = pd.read_csv(os.path.join(args.data_dir, subject), header=None)
        dev_df = all_df[: args.ntrain]
        test_df = all_df[args.ntrain:]
        if args.fixed_answer != -1:
            dev_df = fix_answer(dev_df, args.fixed_answer)
            test_df = fix_answer(test_df, args.fixed_answer)
        elif args.fixed_example_answer != -1:
            dev_df = fix_answer(dev_df, args.fixed_example_answer)
        elif args.fixed_question_answer != -1:
            test_df = fix_answer(test_df, args.fixed_question_answer)

        cors, acc, probs = eval(args, subject, model, tokenizer, dev_df, test_df)
        subcats = subcategories[subject]
        for subcat in subcats:
            subcat_cors[subcat].append(cors)
            for key in categories.keys():
                if subcat in categories[key]:
                    cat_cors[key].append(cors)
        all_cors.append(cors)

        test_df["{}_correct".format(args.model)] = cors
        for j in range(probs.shape[1]):
            choice = choices[j]
            test_df["{}_choice_{}_probs".format(args.model, choice)] = probs[:, j]
        test_df.to_csv(
            os.path.join(
                args.save_dir, "results_{}".format(args.model), "{}.csv".format(subject)
            ),
            index=None,
        )
    with open(os.path.join(save_result_dir, 'summary.txt'), 'w') as f:
        f.write("\n------subcategory level sta------\n")
        for subcat in subcat_cors:
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


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ntrain", "-k", type=int, default=5)
    parser.add_argument("--ngpu", "-g", type=int, default=1)
    parser.add_argument("--data_dir", "-d", type=str, default="data")
    parser.add_argument("--save_dir", "-s", type=str, default="results")
    parser.add_argument("--options_num", "-o", type=int, default=4)
    parser.add_argument("--use_rare_symbol", "-r", type=bool, default=False)
    parser.add_argument("--fixed_answer", "-f", type=int, default=-1)
    parser.add_argument("--fixed_example_answer", "-e", type=int, default=-1)
    parser.add_argument("--fixed_question_answer", "-q", type=int, default=-1)
    parser.add_argument(
        "--model",
        "-m",
        type=str,
        default="meta-llama/Llama-2-7b-hf",
    )
    args = parser.parse_args()
    main(args)
