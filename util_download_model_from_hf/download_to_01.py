from transformers import AutoModelForCausalLM, AutoTokenizer
import os

# 模型名称
# model_name = "meta-llama/Meta-Llama-3-70B"
model_name = "mistralai/Ministral-8B-Instruct-2410"

# 保存模型的路径
# save_directory = "/ML-A100/team/mm/zhangge/"
save_directory = "/data/yubowang/models/Ministral-8B-Instruct-2410"
os.makedirs(save_directory, exist_ok=True)
# 加载模型和分词器
model = AutoModelForCausalLM.from_pretrained(model_name)
tokenizer = AutoTokenizer.from_pretrained(model_name)

# 保存模型和分词器到指定路径
model.save_pretrained(save_directory)
tokenizer.save_pretrained(save_directory)


model_name = "Qwen/Qwen1.5-72B"

# 保存模型的路径
# save_directory = "/ML-A100/team/mm/zhangge/"
save_directory = "/ML-A800/models/Qwen1.5-72B"
os.makedirs(save_directory, exist_ok=True)
# 加载模型和分词器
model = AutoModelForCausalLM.from_pretrained(model_name)
tokenizer = AutoTokenizer.from_pretrained(model_name)

# 保存模型和分词器到指定路径
model.save_pretrained(save_directory)
tokenizer.save_pretrained(save_directory)

model_name = "Qwen/Qwen1.5-110B-Chat"

# 保存模型的路径
# save_directory = "/ML-A100/team/mm/zhangge/"
save_directory = "/ML-A800/models/Qwen1.5-110B-Chat"
os.makedirs(save_directory, exist_ok=True)
# 加载模型和分词器
model = AutoModelForCausalLM.from_pretrained(model_name)
tokenizer = AutoTokenizer.from_pretrained(model_name)

# 保存模型和分词器到指定路径
model.save_pretrained(save_directory)
tokenizer.save_pretrained(save_directory)
