import io
import os
from openai import OpenAI
from langchain.tools import StructuredTool, Tool
from io import BytesIO
import requests
import json
from io import BytesIO

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
    client = OpenAI()

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
