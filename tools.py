import io
import os
from openai import OpenAI
from langchain.tools import StructuredTool, Tool
from io import BytesIO
import requests
import json
from io import BytesIO
import base64
import chainlit as cl


def get_image_name():
    """
    We need to keep track of images we generate, so we can reference them later
    and display them correctly to our users.
    """
    image_count = cl.user_session.get("image_count")
    if image_count is None:
        image_count = 0
    else:
        image_count += 1

    cl.user_session.set("image_count", image_count)

    return f"image-{image_count}"


def _generate_image(prompt: str):
    """
    This function is used to generate an image from a text prompt using
    DALL-E 3.

    We use the OpenAI API to generate the image, and then store it in our
    user session so we can reference it later.
    """
    client = OpenAI(api_key=cl.user_session.get("api_key"))

    response = client.images.generate(
        model="dall-e-3",
        prompt=prompt,
        size="1024x1024",
        quality="standard",
        n=1,
    )

    image_payload = requests.get(response.data[0].url, stream=True)

    image_bytes = BytesIO(image_payload.content)

    print(type(image_bytes))

    name = get_image_name()
    cl.user_session.set(name, image_bytes.getvalue())
    cl.user_session.set("generated_image", name)
    return name


def generate_image(prompt: str):
    image_name = _generate_image(prompt)
    return f"Here is {image_name}."


# this is our tool - which is what allows our agent to generate images in the first place!
# the `description` field is of utmost imporance as it is what the LLM "brain" uses to determine
# which tool to use for a given input.
generate_image_format = '{{"prompt": "prompt"}}'
generate_image_tool = Tool.from_function(
    func=generate_image,
    name="GenerateImage",
    description=f"Useful to create an image from a text prompt. Input should be a single string strictly in the following JSON format: {generate_image_format}",
    return_direct=True,
)


def gpt_vision_call(image_id: str):
    #cl.user_session.set("image_id", image_id)
    print("image_id", image_id)
    client = OpenAI(api_key=cl.user_session.get("api_key"))
    image_history = cl.user_session.get("image_history")
    stream = client.chat.completions.create(
        model="gpt-4-vision-preview",
        messages=image_history,
        max_tokens=350,
        stream=False,
    )

    return stream

def handle_image_history(msg):
    image_history = cl.user_session.get("image_history")
    image_base64 = None
    image_base64 = process_images(msg)
    
    if image_base64:
        # add the image to the image history
        image_history.append(
        {
            "role": "user",
            "content": [
                    {"type": "text", "text": msg.content},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{image_base64}",
                            "detail": "low"
                        }
                    },
                ],
            }
        )
        cl.user_session.set("image_history", image_history)


def process_images(msg: cl.Message):
    # Processing images exclusively
    images = [file for file in msg.elements if "image" in file.mime]

    # Accessing the bytes of a specific image
    image_bytes = images[0].content # take the first image just for demo purposes
    
    # we need base64 encoded image
    image_base64 = base64.b64encode(image_bytes).decode('utf-8')
    return image_base64

describe_image_format = '{{"image_id": "image_id"}}'
describe_image_tool = Tool.from_function(
    func=gpt_vision_call,
    name="DescribeImage",
    description=f"Useful to describe an image. Input should be a single string strictly in the following JSON format: {describe_image_format}",
    return_direct=False,
)



async def wait_for_key():
    res = await cl.AskUserMessage(content="Send an Openai API KEY to start. [https://platform.openai.com/api-keys](https://platform.openai.com/api-keys). e.g. sk-IY8Wl.....1cXD8", timeout=600).send()
    if res:
        await cl.Message(content="setting up...", indent=1).send()
        # check if the key is valid
        client = OpenAI(api_key=res["content"])
        try:
            stream = client.chat.completions.create(
                model="gpt-3.5-turbo-1106",
                messages=[{"role": "system", "content": "test"}],
                max_tokens=1,
            )
            if stream:
                await cl.Message(content="API_KEY setted, you can start chatting!", indent=1).send()
                cl.user_session.set("api_key", res["content"])
        except Exception as e:
            await cl.Message(content=f"{e}", indent=1).send()
            return await wait_for_key()
        return await cl.Message(content="✅ API KEY works! ✅ you can start chatting! 💬").send()
    else:
        return await wait_for_key()