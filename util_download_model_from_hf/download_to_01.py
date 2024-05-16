from transformers import AutoModelForCausalLM, AutoTokenizer

# 模型名称
# model_name = "meta-llama/Meta-Llama-3-70B"
model_name = "Qwen/Qwen1.5-110B"

# 保存模型的路径
# save_directory = "/ML-A100/team/mm/zhangge/"
save_directory = "/ML-A800/models/"

# 加载模型和分词器
model = AutoModelForCausalLM.from_pretrained(model_name)
tokenizer = AutoTokenizer.from_pretrained(model_name)

# 保存模型和分词器到指定路径
model.save_pretrained(save_directory)
tokenizer.save_pretrained(save_directory)


model_name = "Qwen/Qwen1.5-72B"

# 保存模型的路径
# save_directory = "/ML-A100/team/mm/zhangge/"
save_directory = "/ML-A800/models/"

# 加载模型和分词器
model = AutoModelForCausalLM.from_pretrained(model_name)
tokenizer = AutoTokenizer.from_pretrained(model_name)

# 保存模型和分词器到指定路径
model.save_pretrained(save_directory)
tokenizer.save_pretrained(save_directory)


