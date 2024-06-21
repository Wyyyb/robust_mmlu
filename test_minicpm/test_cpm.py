from chat import MiniCPMVChat, img2base64
import torch
import json

torch.manual_seed(0)

chat_model = MiniCPMVChat('openbmb/MiniCPM-Llama3-V-2_5')

im_64 = img2base64('test_data/test_0614_1.png')

# First round chat
msgs = [{"role": "user", "content": "Parse and extract the table information from the image."}]

inputs = {"image": im_64, "question": json.dumps(msgs)}
answer = chat_model.chat(inputs)
print("answer1:\n", answer)

# Second round chat
# pass history context of multi-turn conversation
msgs.append({"role": "assistant", "content": answer})
msgs.append({"role": "user", "content": "How many products are in this image?"})

inputs = {"image": im_64, "question": json.dumps(msgs)}
answer = chat_model.chat(inputs)
print("answer2:\n", answer)


