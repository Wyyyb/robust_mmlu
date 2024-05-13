

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








