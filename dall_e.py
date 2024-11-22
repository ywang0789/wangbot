import os

import requests
from openai import OpenAI

import utils
from secret.secret import OPENAI_API_KEY

# image model settings
IMG_MODEL = "dall-e-3"
IMG_SIZE = "1024x1024"
IMG_QUALITY = "standard"
IMG_FILE_DIR = "./secret/images/"


class DallE:
    def __init__(self):
        self._client = OpenAI(api_key=OPENAI_API_KEY)

    def generate_image(self, prompt: str) -> str:
        """Downloads and returns an image local path"""

        # get generated image url
        response = self._client.images.generate(
            model=IMG_MODEL,
            prompt=prompt,
            size=IMG_SIZE,
            quality=IMG_QUALITY,
            n=1,
        )
        img_url = response.data[0].url

        # create dir is not exist
        if not os.path.exists(IMG_FILE_DIR):
            os.makedirs(IMG_FILE_DIR)

        # download and save image
        img_response = requests.get(img_url)
        file_path = os.path.join(IMG_FILE_DIR, utils.get_unique_str() + ".png")
        try:
            with open(file_path, "wb") as f:
                f.write(img_response.content)
        except:
            raise Exception("Could not save image.")

        return file_path


if __name__ == "__main__":
    b = DallE()
    print(b.generate_image("a cute cat"))
