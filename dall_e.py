import os

import openai
import requests

import utils
from secret.keys import OPENAI_API_KEY

# image model settings
IMG_MODEL = "dall-e-3"
IMG_SIZE = "1024x1024"
IMG_QUALITY = "standard"
IMG_FILE_DIR = "./secret/images/"


class DallE:
    def __init__(self):
        self.client = openai.OpenAI(api_key=OPENAI_API_KEY)

    def get_img_response(self, user_input: str):
        """Downloads and returns an image path of url response"""

        # get response
        response = self.client.images.generate(
            model=IMG_MODEL,
            prompt=user_input,
            size=IMG_SIZE,
            quality=IMG_QUALITY,
            n=1,
        )

        # get image url
        image_url = response.data[0].url

        # Download and save image
        img_response = requests.get(image_url)

        # create dir is not exist
        if not os.path.exists(IMG_FILE_DIR):
            os.makedirs(IMG_FILE_DIR)

        file_path = IMG_FILE_DIR + utils.get_unique_str() + ".png"

        try:
            # write
            with open(file_path, "wb") as f:
                f.write(img_response.content)
        except:
            raise Exception("Could not save image.")

        return file_path


if __name__ == "__main__":
    b = DallE()
    print(b.get_img_response("a cute cat"))
