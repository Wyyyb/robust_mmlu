

def prompt_format_examples(prompt_format, question, options):
    prompt = "Question:\n"
    choices = "ABCDEFGHIJ"
    # if prompt_format in [1, 2, 3, 4]:
    #     prompt += "Question:\n"
    # elif prompt_format in [5]:
    #     prompt += "Q: "
    prompt += question + "\n"
    if prompt_format in [1, 2, 3, 4, 5, 6, 7, 8]:
        prompt += "Options:\n"
    for i, each in enumerate(options):
        if prompt_format in [1]:
            prompt += f"({choices[i]}) {options[i]}\n"
        else:
            prompt += f"{choices[i]}. {options[i]}\n"
    if prompt_format in [2]:
        prompt += "Correct answer is: "
    elif prompt_format in [3]:
        prompt += "Your choice is "
    elif prompt_format in [4]:
        prompt += "The most likely option is "
    elif prompt_format in [5]:
        prompt += "The correct answer is option "
    else:
        prompt += "Answer: "
    return prompt


def prompt_format_examples_0516(prompt_format, question, options):
    if prompt_format >= 1000:
        ins_format = prompt_format
    else:
        ins_format = -1
    choices = "ABCDEFGHIJ"
    # 决定是否Question:与question是否放在同一行
    if prompt_format % 4 == 0 or ins_format in [1000, 1001, 1002, 1003]:
        prompt = "Question:\n"
    elif prompt_format % 4 == 1:
        prompt = "Question: "
    elif prompt_format % 4 == 2:
        prompt = "**Question**: "
    # elif prompt_format % 4 == 3:
    else:
        prompt = "Q: "

    prompt += question
    prompt_format = prompt_format // 4
    # option_prefix
    if prompt_format % 3 == 0 or ins_format in [1000, 1001, 1002, 1003]:
        option_prefix_1 = ""
        option_prefix_2 = ". "
    elif prompt_format % 3 == 1:
        option_prefix_1 = "("
        option_prefix_2 = ") "
    # elif prompt_format % 3 == 2:
    else:
        option_prefix_1 = ""
        option_prefix_2 = ") "

    prompt_format = prompt_format // 3
    # option_postfix

    if prompt_format % 3 == 1 or ins_format in [1000, 1001, 1002, 1003]:
        option_postfix = "\n"
    elif prompt_format % 3 == 0:
        option_postfix = ", "
    else:
        option_postfix = " "

    if "\n" in option_postfix:
        prompt += "\nOptions:\n"
    else:
        prompt += " "

    prompt_format = prompt_format // 3
    for i, each in enumerate(options):
        prompt += f"{option_prefix_1}{choices[i]}{option_prefix_2}{options[i]}{option_postfix}"

    prompt += "\n"
    if ins_format == 1000:
        answer_prefix = "Answer: "
    elif ins_format == 1001:
        answer_prefix = "Your choice: "
    elif ins_format == 1002:
        answer_prefix = "The Best Choice: "
    elif ins_format == 1003:
        answer_prefix = "The most likely option is "
    # normal
    elif prompt_format % 6 == 0:
        answer_prefix = "Answer: "
    elif prompt_format % 6 == 1:
        answer_prefix = "**Answer**:"
    elif prompt_format % 6 == 2:
        answer_prefix = "**Correct Answer**: "
    elif prompt_format % 6 == 3:
        answer_prefix = "Your choice: "
    elif prompt_format % 6 == 4:
        answer_prefix = "The Best Choice: "
    # elif prompt_format % 6 == 5:
    else:
        answer_prefix = "The most likely option is "

    prompt += answer_prefix
    return prompt






