import os
import base64
import time
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

client = OpenAI(
    api_key="GEMINI_API_KEY",
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/")



def generate_caption(image_path, model):


    with open(image_path, "rb") as image_file:
        image_base64 = base64.b64encode(image_file.read()).decode("utf-8")

    response = client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "What is in this image?",
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{image_base64}"
                        },
                    },
                ],
            }
        ],
    )


    try:
      caption = response.choices[0].message
    except AttributeError as e:
      caption = f"Error extracting content: {e}"

    return caption


def process_images_in_directory(directory_path):

    models = ["gemini-1.5-pro", "gemini-1.5-flash"]

    for file_name in os.listdir(directory_path):
        file_path = os.path.join(directory_path, file_name)


        if file_name.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):


            for model in models:

                try:

                    caption = generate_caption(file_path, model=model)
                    print(f"  Model: {model}")
                    print(f" Processing file: {file_name}")
                    print(f"  Caption: {caption}\n")
                except Exception as e:
                    print(f"  Error using model {model} for file {file_name}: {e}")


                time.sleep(35)



if __name__ == "__main__":
    directory_path = <insert>
    process_images_in_directory(directory_path)
