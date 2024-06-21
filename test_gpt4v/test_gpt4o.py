import os
from openai import OpenAI
from openai import AzureOpenAI
import json
import re
import random
from tqdm import tqdm
import time
import base64

API_KEY = '1354fba3c4c544e995860360e0c61376'

my_client = AzureOpenAI(
  azure_endpoint="https://waterloo-gpt-turbo3.openai.azure.com/",
  api_key=API_KEY,
  api_version="2024-02-01"
)


def call_gpt_4o():
    start = time.time()
    IMAGE_PATH = "test_data/test_0614_1.png"
    encoded_image = base64.b64encode(open(IMAGE_PATH, 'rb').read()).decode('ascii')
    message_text = [
        {
            "role": "system",
            "content": [
                {"type": "text",
                 "text": "You are an AI assistant that helps people parse and extract the table "
                         "information from the image."}]
        },
        {
            "role": "user",
            "content": [
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/jpeg;base64,{encoded_image}"
                    }
                },
                {
                    "type": "text",
                    "text": "用中文输出表格中的信息"
                }
            ]
        },
    ],
    completion = my_client.chat.completions.create(
      model="gpt-4o",
      messages=message_text,
      temperature=0,
      max_tokens=4000,
      top_p=1,
      frequency_penalty=0,
      presence_penalty=0,
      # stop=['Question:']
    )
    print("cost time", time.time() - start)
    return completion.choices[0].message.content


result = call_gpt_4o()
print("result", result)



