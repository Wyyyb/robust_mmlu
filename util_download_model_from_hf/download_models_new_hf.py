from huggingface_hub import snapshot_download
import os


def download_model_from_hf_hub(repo_id, local_dir, hf_token):
    try:
        os.makedirs(local_dir, exist_ok=True)
        snapshot_download(repo_id=repo_id,
                          local_dir=local_dir,
                          token=hf_token)
        print(f"Model files have been downloaded to: {local_dir}")
    except Exception as e:
        print(f"An error occurred while downloading the model: {str(e)}")


# 用户变量设置
# repo_id = "meta-llama/Llama-3.2-90B-Vision"
repo_id = "mistralai/Ministral-8B-Instruct-2410"
# local_dir = "/gpfs/public/research/xy/yubowang/models/Idefics3-8B-Llama3"
local_dir = "/data/yubowang/models/Ministral-8B-Instruct-2410"
hf_token = "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"  # 替换为你的 Hugging Face API token

# 调用函数
download_model_from_hf_hub(repo_id, local_dir, hf_token)
