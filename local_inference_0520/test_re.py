import re


def extract_again(text):
    match = re.search(r'.*[aA]nswer:\s*([A-J])', text)
    if match:
        return match.group(1)
    else:
        return None


s = "Answer: E. 3.38 * 10"
res = extract_again(s)
print(res)
