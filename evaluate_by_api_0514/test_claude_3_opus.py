import openai
from openai import OpenAI

API_BASE = "https://api.lingyiwanwu.com"
# API_BASE = "https://api.pre.lingyiwanwu.com/"
# API_BASE = "https://api.01ww.xyz"
API_KEY = "ef798a2b5d834a1b8d6f2e69d83b22c7"
# API_KEY = "191d4c83d53245848862382a4187a49c"

client = OpenAI(
    # defaults to os.environ.get("OPENAI_API_KEY")
    api_key=API_KEY,
    base_url=API_BASE
)

completion = client.chat.completions.create(
    model="claude-3-opus-20240229",  # 这里填写模型名称（yi-34b-chat-0205 / yi-34b-chat-200k），注意全部小写。
    # model="claude-3-sonnet-20240229",
    messages=[
        {
            "role": "user",
            "content": "Hello there."
        },
        {
            "role": "assistant",
            "content": "Hi, I'\''m Claude. How can I help you?"
        },
        {
            "role": "user",
            "content": "Can you explain LLMs in plain English?"
        }
    ]

)
print(completion)

#API输出
#ChatCompletion(id='cmpl-095ae978', choices=[Choice(finish_reason='stop', index=0, logprobs=None, message=ChatCompletionMessage(content='花粉过敏确实是一件让人困扰的事情。花粉季节里，空气中的花粉颗粒增多，容易引起过敏反应，导致鼻子痒、打喷嚏、流鼻涕等症状。\n\n为了缓解这些症状，你可以尝试以下方法：\n\n1. 避免接触花粉：尽量减少户外活动，特别是在花粉高峰时段，如中午和下午。如果必须外出，可以戴上口罩以减少花粉的吸入。\n\n2. 保持室内清洁：关闭门窗，使用空调或空气净化器来过滤花粉。定期清洁家居，特别是床上用品、窗帘和地毯，以减少花粉的积累。\n\n3. 洗鼻：使用盐水洗鼻可以帮助清洗鼻腔中的花粉和其他过敏原。这可以缓解鼻塞和痒感。\n\n4. 药物治疗：抗过敏药物如抗组胺药和鼻喷剂可以缓解过敏症状。但是，在使用任何药物之前，最好咨询医生或药师。\n\n5. 饮食调整：有些食物可能有助于缓解过敏症状，如蜂蜜、姜、大蒜等。但请注意，这些食物并不适用于所有人，建议在咨询医生后再尝试。\n\n如果你发现自己对花粉过敏的情况比较严重，建议你咨询过敏专科医生，进行过敏原测试，并获得专业的治疗建议。', role='assistant', function_call=None, tool_calls=None))], created=1618121, model='yi-34b-chat-0205', object='chat.completion', system_fingerprint=None, usage=CompletionUsage(completion_tokens=279, prompt_tokens=93, total_tokens=372))
