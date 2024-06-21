import os
import requests
import base64

MODEL = "gpt-4v-turbo"
AZURE_END_POINT = "https://waterloo-gpt-vision-4.openai.azure.com/"
AZURE_OPENAI_API_KEY = '53defdd38b7843378f7be58406c33f67'
API_VERSION = "2024-02-15-preview"

# Configuration
GPT4V_ENDPOINT = f"{AZURE_END_POINT}/openai/deployments/{MODEL}/chat/completions?api-version={API_VERSION}"

IMAGE_PATH = "test_data/test_0614_1.png"

encoded_image = base64.b64encode(open(IMAGE_PATH, 'rb').read()).decode('ascii')
headers = {
    "Content-Type": "application/json",
    "api-key": AZURE_OPENAI_API_KEY,
}

# Payload for the request
payload = {
  "messages": [
    {
      "role": "system",
      "content": [
          {"type": "text",
           "text": "You are an AI assistant that helps people parse and extract the table information from the image."}]
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
  "temperature": 0.7,
  "top_p": 0.95,
  "max_tokens": 800
}

# Send request
try:
    response = requests.post(GPT4V_ENDPOINT, headers=headers, json=payload)
    response.raise_for_status()  # Will raise an HTTPError if the HTTP request returned an unsuccessful status code
except requests.RequestException as e:
    raise SystemExit(f"Failed to make the request. Error: {e}")


output = response.json()['choices'][0]['message']['content']
print(output)








