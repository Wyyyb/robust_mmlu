import time
import transformers
import torch
from vllm import LLM, SamplingParams


def test_vllm():
    max_model_len, tp_size = 2048, 2
    prompt = ""
    with open("cot.txt", "r") as fi:
        for line in fi.readlines():
            prompt += line
    model_name = "meta-llama/Llama-2-7b-hf"
    tokenizer = transformers.AutoTokenizer.from_pretrained(model_name)
    stop_words = "Question:"
    stop_tokens = tokenizer.encode(stop_words, add_special_tokens=False)
    print("stop_tokens", stop_tokens)
    llm = LLM(model=model_name, gpu_memory_utilization=0.7)
    sampling_params = SamplingParams(temperature=0, max_tokens=256,
                                     stop=["Question:"])
    for i in range(10):
        start = time.time()
        outputs = llm.generate([prompt for _ in range(4)], sampling_params)
        for output in outputs:
            prompt = output.prompt
            generated_text = output.outputs[0].text
            # print(f"Prompt: {prompt!r}, Generated text: {generated_text!r}")
            if generated_text.startswith(prompt):
                answer = generated_text.replace(prompt, "")
                print("answer", answer)
            else:
                print("generated_text", generated_text)
        print(i, "vllm cost time", time.time() - start)


def test_llama():
    model_name = "meta-llama/Llama-2-7b-hf"
    prompt = ""
    with open("cot.txt", "r") as fi:
        for line in fi.readlines():
            prompt += line
    tokenizer = transformers.AutoTokenizer.from_pretrained(model_name)
    inputs = tokenizer(prompt, return_tensors="pt")
    inputs = {key: value.cuda() for key, value in inputs.items()}
    model = transformers.AutoModelForCausalLM.from_pretrained(model_name,
                                                              device_map="auto",
                                                              torch_dtype=torch.bfloat16)
    for i in range(10):
        start = time.time()
        output = model.generate(**inputs, max_new_tokens=256, num_return_sequences=1)
        answer = tokenizer.decode(output[0], skip_special_tokens=True)
        # print("ori answer", answer)
        if answer.startswith(prompt):
            answer = answer.replace(prompt, "")
        print("answer", answer)
        print(i, "llama cost time", time.time() - start)


if __name__ == "__main__":
    test_vllm()
    # test_llama()
