import re
import json
import string


def find_special_characters(input_string):
    special_characters = ''.join(set(c for c in input_string if not c.isprintable()))
    print("special_charact", special_characters)
    # Include all English letters, digits, and the extended set of punctuation marks
    allowed_characters = string.ascii_letters + string.digits + string.punctuation + ' '
    # allowed_characters += '\n'+'×'

    # Define the pattern to exclude these allowed characters
    pattern = re.compile(f'[^{re.escape(allowed_characters)}]')

    # Find all substrings that match the pattern (special characters)
    special_characters = pattern.findall(input_string)

    # Remove duplicates by converting to a set, then back to a list
    unique_special_characters = list(set(special_characters))

    return unique_special_characters


def cleanup(input_string):
    allowed_chars_regex = r'[A-Za-z0-9\s.,?!;:\'\"]+'

    # 使用正则表达式找到所有匹配的字符
    matches = re.findall(allowed_chars_regex, input_string)

    # 将匹配的字符连接成一个新的字符串
    cleaned_string = ''.join(matches)

    return cleaned_string


def check_file_1(file_path):
    output_path = file_path.replace(".json", "_test.json")
    res = []
    with open(file_path, 'r') as fi:
        data = json.load(fi)
    for each in data:
        curr = {"data": {}}
        for k, v in each["data"].items():
            if not isinstance(v, str):
                curr["data"][k] = v
                continue
            curr["data"][k] = cleanup(v)
        res.append(curr)
    with open(output_path, "w", encoding="utf-8") as fo:
        fo.write(json.dumps(res))


check_file_1("data/stemez_label_data_5.json")



