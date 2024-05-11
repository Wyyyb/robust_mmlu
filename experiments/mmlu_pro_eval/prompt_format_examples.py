

def prompt_format_examples(prompt_format, question, options):
    prompt = ""
    choices = "ABCDEFGHIJ"
    if prompt_format in [1, 2, 3, 4]:
        prompt += "Question:\n"
    elif prompt_format in [5]:
        prompt += "Q: "
    prompt += question + "\n"
    if prompt_format in [1, 2, 3]:
        prompt += "Options:\n"
    for i, each in enumerate(options):
        if prompt_format in [1]:
            prompt += f"({choices[i]}) {options[i]}\n"
        else:
            prompt += f"{choices[i]}. {options[i]}\n"
    if prompt_format in [2]:
        prompt += "Correct option is: "
    elif prompt_format in [3]:
        prompt += "Your choice is "
    elif prompt_format in [4]:
        prompt += "Answer is"
    elif prompt_format in [5]:
        prompt += "A: "
    elif prompt_format in [6]:
        prompt += "Answer: "
    else:
        prompt += "Answer:"
    return prompt








