import anthropic
import os
import base64
import time
from dotenv import load_dotenv

load_dotenv()
CLAUDE_API_KEY = os.getenv("CLAUDE_API_KEY")

client = anthropic.Anthropic(api_key=CLAUDE_API_KEY)


def generate_caption(image_path, model):
    """
    Generate a caption for the given image using the specified model.

    Args:
        image_path (str): Path to the image file.
        model (str): The model to use for caption generation.

    Returns:
        str: The generated caption or an error message.
    """
    try:

        with open(image_path, "rb") as image_file:
            image_base64 = base64.b64encode(image_file.read()).decode("utf-8")

        image1_media_type = "image/jpeg"
        image1_data = image_base64


        response = client.messages.create(
            model=model,
            max_tokens=1024,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "image",
                            "source": {
                                "type": "base64",
                                "media_type": image1_media_type,
                                "data": image1_data,
                            },
                        },
                        {
                            "type": "text",
                            "text": "Describe this image."
                        }
                    ],
                }
            ],
        )


        caption = response
    except AttributeError as e:
        caption = f"Error extracting content: {e}"

    return caption


def process_images_in_directory(directory_path):
    """
    Process all images in the specified directory and generate captions using all models.

    Args:
        directory_path (str): Path to the directory containing images.
    """

    models = ["claude-3-5-sonnet-20241022", "claude-3-opus-20240229", "claude-3-sonnet-20240229"]  #

    for file_name in os.listdir(directory_path):
        file_path = os.path.join(directory_path, file_name)


        if file_name.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
            print(f"\nProcessing file: {file_name}")

            for model in models:
                print(f"Using model: {model}")
                try:

                    caption = generate_caption(file_path, model=model)
                    print(f"  Caption: {caption}\n")
                except Exception as e:
                    print(f"  Error using model {model} for file {file_name}: {e}")


                time.sleep(10)



if __name__ == "__main__":
    directory_path = <insert>
    process_images_in_directory(directory_path)
