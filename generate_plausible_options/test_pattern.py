import re

def extract_options(text):
    pattern = r'\([ABCD]\) (.*?)(?=\([ABCD]\)|$)'
    matches = re.findall(pattern, text)
    return matches

# 测试代码
texts = [
    "(A) (ii) and (iv) only (B) (i) and (iii) only (C) (i), (ii), and (iii) only (D) (i), (ii), (iii), and (iv)",
    "(A) (5 x 4) x (6 x 5) (B) (5 x 5) + (5 x 4) (C) (5 x 5) + (5 x 9) (D) (5 x 9) x (6 x 9)",
    "(A) ~Pd (B) (∀x)(Px ∨ ~Dx) (C) (∀x)(Px ⊃ ~Dx) (D) ~Dp"
]

for text in texts:
    print(extract_options(text))