import os
import asyncio
import base64
from anthropic import Anthropic


# Function to encode the image
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")


def make_content(text, image_paths):
    text_elem = {
        "type": "text",
        "text": text,
    }

    content = [text_elem]
    for image_path in image_paths:
        image_fmt = os.path.splitext(image_path)[1]
        if image_fmt not in [".jpg", ".jpeg", ".png"]:
            raise ValueError(f"Unsupported image format: {image_fmt}")
        else:
            if image_fmt == ".jpg":
                image_fmt = "jpeg"

        base64_image = encode_image(image_path)
        image_elem = {
            "type": "image",
            "source":
            {
                "type": "base64",
                "media_type": f"image/{image_fmt}",
                "data": base64_image,
            }
        }
        content.append(image_elem)

    return content


# async def request(title, description, asr, image_paths) -> None:
def request(prompt, image_paths, timeout=60, max_tokens=100, model_name="sonnet"):
    name2model = {
        "haiku": "claude-3-haiku-20240307",
        "sonnet": "claude-3-sonnet-20240229",
        "opus": "claude-3-opus-20240229"
    }
    model = name2model[model_name]

    api_key = "multimodel-lidongxu"
    # api_key = "claude-eval"
    base_url = "https://api.pre.lingyiwanwu.com/v1/messages "

    client = Anthropic(
        base_url=base_url,
        api_key=api_key,
    )

    response = client.messages.create(
        model=model,
        messages=[
            {
                "role": "user",
                "content": "hello",
            }  # Add closing square bracket here
        ],  # Add closing square bracket here
        max_tokens=max_tokens,
        timeout=timeout,
    )

    return response


if __name__ == "__main__":
    title = "test title"
    description = "test description"
    asr = "test asr"
    image_paths = [
        "/ML-A100/team/mm/lidongxu/workspace/multimodal-yi/scripts/video_preprocess/clips_ytt180m_v2/--wO4RopA-k/--wO4RopA-k-0000-000109-q.jpg"
    ]

    # response = asyncio.run(request(title, description, asr, image_paths))
    response = request(title, description, asr, image_paths, model_name="opus")

    print("async call done")
    import pdb

    pdb.set_trace()
    print(response.choices[0])


# response = asyncio.run(request())

# print("async call done")
# import pdb

# pdb.set_trace()
# print(response.choices[0])