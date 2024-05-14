import openai
from openai import OpenAI
from anthropic import Anthropic

API_BASE = "https://api.lingyiwanwu.com"
# API_BASE = "https://api.pre.lingyiwanwu.com/"
# API_BASE = "https://api.01ww.xyz"
# API_KEY = "ef798a2b5d834a1b8d6f2e69d83b22c7"
# API_KEY = "126df074e908436e8a171e445fe702cb"
# API_KEY = "bdfad0935717497e8a4eca4eca1da405"
API_KEY = "191d4c83d53245848862382a4187a49c"

client = OpenAI(
    # defaults to os.environ.get("OPENAI_API_KEY")
    api_key=API_KEY,
    base_url=API_BASE
)


def request(prompt, timeout=60, max_tokens=2000):
    # api_key = "multimodel-lidongxu"
    api_key = API_KEY

    # client = OpenAI(
    client = Anthropic(
        # base_url="https://api.01ww.xyz/v1",
        base_url="https://api.01ww.xyz/",
        api_key=api_key,
    )

    # response = client.chat.completions.create(
    response = client.messages.create(
        model="claude-3-opus-20240229",
        # model="yi-34b-chat-0205",
        # model="claude-3-haiku-20240307",
        messages=[
            {
                "role": "user",
                "content": prompt
            }  # Add closing square bracket here
        ],  # Add closing square bracket here
        max_tokens=max_tokens,
        timeout=timeout,
    )

    return response


request("hello")

