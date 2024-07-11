from collections import defaultdict
import datasets

test = datasets.load_dataset("TIGER-Lab/MMLU-Pro", split="test")

map_result = []
count = 0
for item in test:
    key = (item["category"], item["question"], item["answer"], ", ".join(item["options"]))
    if key not in map_result:
        map_result.append(key)

    else:
        count += 1
        print(key)

print(count)



