import os
from openai import AzureOpenAI
import csv
import re
import random
from tqdm import tqdm
import json

API_KEY = '786f8c1ff30a4c4b9f9b8917f2f5191b'

my_client = AzureOpenAI(
    azure_endpoint="https://waterloo-gpt4.openai.azure.com/",
    api_key=API_KEY,
    api_version="2024-02-15-preview"
)


def call_gpt_4(client, instruction, inputs):
    message_text = [{"role": "user", "content": instruction + inputs}]
    completion = client.chat.completions.create(
        model="gpt-4",
        messages=message_text,
        temperature=0.0,
        max_tokens=2000,
        top_p=0.95,
        frequency_penalty=0,
        presence_penalty=0,
        stop=None
    )
    return completion.choices[0].message.content


def read_csv_file(file_path):
    with open(file_path, mode='r', encoding='utf-8') as file:
        csv_reader = csv.reader(file)
        # Skip the header if there is one
        # next(csv_reader, None)
        data = list(csv_reader)
    return data


def write_2dlist_to_csv(data, file_name):
    with open(file_name, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerows(data)


def single_request_gpt(question, options):
    prompt_1 = f"I need to check if the multiple-choice questions for the XX subject are appropriate. \
    Please assist me with the following tasks: 1. Evaluate whether the following question is suitable as a \
    multiple-choice question in the relevant subject. Calculation problems are generally \
    considered acceptable, while proof problems and programming questions involving large blocks of code are usually \
    deemed inappropriate. 2. If it's not suitable, provide a brief reason; if it is suitable, no response is needed. \
    3. If it's not suitable, help me rewrite the \
    question and options to make it a meaningful multiple-choice question. 4. Provide the answer and a brief \
    analysis. 5. Translate the rewritten question, options and the analysis into Chinese. "

    prompt_2 = """Return your answer in JSON format like: \
{
    "suitable": "True/False",
    "brief reason": "a short reason/None",
    "rewritten question": "the rewritten question/None",
    "rewritten options": "the rewritten options/None",
    "correct answer": "answer/None",
    "brief analysis": "a brief analysis",
    "Chinese translation": "the rewritten question, options and the analysis translation into Chinese"
}
    """

    example_1 = """
    Question: Write a FORTRAN program which uses the modified Euler method to simulate the growth of \
    an isolated species from time t = 0 to t =t_f, if the number of individuals at time t is N(t), N(0) = N_0 \
    and the rate of population change (per unit of time), N, is given by: Ṅ = [K + E(t) - N/M)N](1) where K and \
    M are positive constants and E(t) is a periodic forcing input resulting from seasonal cycles, given by: \
    Case 1: E(t) is sinusoidal with amplitude = A, period = 2π / ω, ω and phase angle φ. \
    Case 2: E(t) is a pulse train of width w, height, h and period Pw, P, h, w > 0, and starting at time t = t_1 .
    Options:
    A. FORTRAN code
    B. C++ code
    C. Java code
    D. Python code
    Response:
    {
    "suitable": "False",
    "brief reason": "The original question requires students to write a complete FORTRAN program, which is too \
    long for a multiple-choice question. Additionally, the question explicitly mentions using the FORTRAN \
    language, while the options include other programming languages, making the answer obvious.",
    "rewritten question": "Which of the following correctly describes the essential steps to be implemented in a \
    FORTRAN program that uses the modified Euler method to simulate the growth of an isolated species from time t = 0 \
    to t = t_f? Consider the change in population size N(t) over time t, with N(0) = N_0 and the rate of \
     population change (per unit time) given by: Ṅ = [K + E(t) - (N/M)]N Here, K and M are positive constants, \
     and E(t) is a periodic forcing input resulting from seasonal cycles. Consider two cases: E(t) is a sinusoidal \
     function with amplitude A, period 2π/ω, and phase angle φ. E(t) is a pulse train with width w, height h, \
     period P, with w, h, P > 0, starting at time t = t_1. To simulate this process using the modified Euler method \
     in a FORTRAN program, which option describes the key steps that must be implemented?",
    "rewritten options": "A. Initialize the population size N(0), set the time step and total simulation time t_f, \
    then iterate to update N(t). B. Write a function to calculate E(t) and call it at each time step to update the\
     population size N(t). C. Use a loop structure to simulate the iteration process from time 0 to t_f, where \
     each step involves calling the modified Euler method. D. Create an array to store the population size N(t) \
     after each iteration and calculate the total population growth at the end of the simulation.",
    "correct answer": "C",
    "brief analysis": "Option C is correct because it accurately describes the core step of iterative computation \
    using the modified Euler method, which involves a loop structure to simulate changes in population size from \
    time 0 to t_f.",
    "Chinese translation": "the rewritten question, options and the analysis translation into Chinese"
}
    """
    ins = prompt_1 + prompt_2 + example_1
    inputs = f"Question: {question}\nOptions: \nA.{options[0]}B.{options[1]}\nC.{options[2]}D.{options[3]}\nResponse:\n"
    response = call_gpt_4(my_client, ins, inputs)
    return response


def is_valid_json(s):
    try:
        json.loads(s)
        return True
    except json.JSONDecodeError:
        return False


def check_exist(question, options, res):
    for each in res:
        if question == each[0] and options == each[1: 5]:
            return True
    return False


def gpt_check_proper():
    input_dir = "data/images_removed_mmlu/"
    output_dir = "data/gpt_check_result/"
    os.makedirs(output_dir, exist_ok=True)
    dir_list = list(os.listdir(input_dir))
    dir_list = sorted(dir_list)
    for file in dir_list:
        if not file.endswith(".csv"):
            continue
        print("Checking", file)
        file_path = os.path.join(input_dir, file)
        data = read_csv_file(file_path)
        output_path = os.path.join(output_dir, file)
        res = []
        if os.path.exists(output_path):
            res = read_csv_file(output_path)
        for each in tqdm(data):
            src = each[6]
            if "stemez" not in src:
                continue
            question = each[0]
            options = each[1:5]
            if check_exist(question, options, res):
                continue
            response = single_request_gpt(question, options)
            if not is_valid_json(response):
                print("invalid json", question)
                curr_res = each + ["-" for _ in range(7)] + [response]
                res.append(curr_res)
                write_2dlist_to_csv(res, output_path)
                continue
            curr = json.loads(response)
            suitable = curr.get("suitable", "")
            brief_reason = curr.get("brief reason", "")
            rewritten_question = curr.get("rewritten question", "")
            rewritten_options = curr.get("rewritten options", "")
            correct_answer = curr.get("correct answer", "")
            brief_analysis = curr.get("brief analysis", "")
            Chinese_translation = curr.get("Chinese translation", "")

            curr_res = each + [suitable, brief_reason, rewritten_question, rewritten_options,
                               correct_answer, brief_analysis, Chinese_translation, response]
            res.append(curr_res)
            write_2dlist_to_csv(res, output_path)


gpt_check_proper()


