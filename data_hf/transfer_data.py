from datasets import load_dataset
from datasets import Dataset


def pull_data():
    dataset = load_dataset("TIGER-Lab/MMLU-Pro")
    test_data, val_data = [], []
    for each in dataset["test"]:
        test_data.append(each)
    for each in dataset["validation"]:
        val_data.append(each)
    return test_data, val_data


def update_data(data):
    return data


def push_data(data):
    test_data, val_data = data
    test_dataset = Dataset.from_list(test_data)
    val_dataset = Dataset.from_list(val_data)
    test_dataset.push_to_hub("TIGER-Lab/MMLU-Pro", split="test")
    val_dataset.push_to_hub("TIGER-Lab/MMLU-Pro", split="validation")


if __name__ == "__main__":
    hf_data = pull_data()
    hf_data = update_data(hf_data)
    push_data(hf_data)


