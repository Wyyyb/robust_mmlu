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
    stop_tokens = tokenizer.encode(stop_words)
    print("stop_tokens", stop_tokens)
    llm = LLM(model=model_name, tensor_parallel_size=tp_size, max_model_len=max_model_len,
              trust_remote_code=True, enforce_eager=True, gpu_memory_utilization=0.9)
    sampling_params = SamplingParams(temperature=0, max_tokens=256,
                                     stop_token_ids=stop_tokens)
    start = time.time()
    outputs = llm.generate([prompt], sampling_params)
    for output in outputs:
        prompt = output.prompt
        generated_text = output.outputs[0].text
        print(f"Prompt: {prompt!r}, Generated text: {generated_text!r}")
    print("vllm cost time", time.time() - start)


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
    start = time.time()
    output = model.generate(**inputs, max_new_tokens=256, num_return_sequences=1)
    answer = tokenizer.decode(output[0], skip_special_tokens=True)
    print("ori answer", answer)
    if answer.startswith(prompt):
        answer = answer.replace(prompt, "")
    print("answer", answer)
    print("llama cost time", time.time() - start)


if __name__ == "__main__":
    test_llama()
    test_vllm()