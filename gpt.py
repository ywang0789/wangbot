"""
For making a gpt chatbot.
"""
import openai
import api_keys
import json
import requests 
import os
import random
import time
SECRET_FILE_DIR = "./secret/"
API_KEY = api_keys.gpt_api_key

# language model settings
LANG_MODEL = "gpt-4-0125-preview"  # "gpt-4-0125-preview" ($0.01 / 1K tokens) OR "gpt-3.5-turbo-1106" ($0.0010 / 1K tokens)
TEXT_PRICING_RATE = 0.0010 / 1000  # change if change model
HISTORY_FILE_DIR = SECRET_FILE_DIR + 'histories/'


# image model settings
IMG_MODEL = "dall-e-3"  # "dall-e-3" ($0.040 / image) OR "dall-e-2 ($0.020 / image")
IMG_SIZE = "1024x1024"
IMG_PRICING_RATE = 0.020  # change if change model
IMG_QUALITY = "standard"
IMG_FILE_DIR = SECRET_FILE_DIR + 'images/'

# system prompts
CONSTANT_SYSTEM_PROMPT = """
You will be speaking with muliple people, their names will be indicated in the message.
the format is:
<name>: <message>
Your responses do not need to follow this format.
"""
# secret system prompt
try: 
    import secret.prompts as prompts
    SYSTEM_PROMPT = prompts.SYSTEM_PROMPT1  # hehe ;)
except: # you do not have the secret sauce
    SYSTEM_PROMPT = 'placeholder'


class gpt:
    """A class that create a gpt that chats and stuff"""

    def __init__(self):
        # set api key
        self.client = openai.OpenAI(api_key=API_KEY)

        # init history for saving context
        self.history = []
        # set system prompt to history
        self.history.append({"role": "system", "content": CONSTANT_SYSTEM_PROMPT})
        self.history.append({"role": "system", "content": SYSTEM_PROMPT})

        # session usage
        self.usage = 0.00

    def get_text_response(self, user_input: str) -> str:
        """Returns a response from GPT. Also updates the history."""

        user_input_len = len(user_input)
        if user_input_len == 0:
            return "Please enter something."

        if user_input_len > 500:
            return "Please keep your input under 500 characters."

        # add user message to history
        self.history.append({"role": "user", "content": user_input})
        # get completion
        response = self.client.chat.completions.create(
            model=LANG_MODEL, messages=self.history
        )
        # extract content from completion
        response_content = response.choices[0].message.content

        # add response to history
        self.history.append({"role": "assistant", "content": response_content})

        # update session usage
        self.usage += response.usage.total_tokens * TEXT_PRICING_RATE

        return response_content

    def get_image_response(self, user_input: str):
        """Downloads and returns an image path of url response from GPT."""
        response = self.client.images.generate(
            model=IMG_MODEL,
            prompt=user_input,
            size=IMG_SIZE,
            quality=IMG_QUALITY,
            n=1,
        )
        # get image url
        image_url = response.data[0].url
        self.usage += IMG_PRICING_RATE

        # Download image
        try:
            img_response = requests.get(image_url)
            # Create a directory to save the image if it doesn't exist
            os.makedirs(SECRET_FILE_DIR, exist_ok=True)

            # generate random number from current time for unique file name
            rand = str(int(time.time()))
            file_path = SECRET_FILE_DIR + rand + IMG_FILE_NAME
            with open(file_path, 'wb') as f:
                f.write(img_response.content)
            return file_path
        except Exception as e:
            return print(e)

    def append_system_prompt(self, new_system_prompt: str):
        """Appends a new system prompt to the history."""
        self.history.append({"role": "assistant", "content": new_system_prompt})

    def overwrite_system_prompt(self, new_system_prompt: str):
        """Sets the system prompt to the new system prompt."""
        self.history[0] = {"role": "system", "content": new_system_prompt}

    def get_usage(self) -> float:
        """Returns the session usage."""
        return self.usage

    def save_history_to(self, file_name: str) -> bool:
        """Saves the history to a json file."""
        try:
            with open(SECRET_FILE_DIR + file_name + ".json", "w") as file:
                json.dump(self.history, file)
        except Exception as e:
            print(e)
            return False

        return True

    def load_history_from(self, file_name: str) -> bool:
        """Loads the history from a json file."""
        try:
            with open(SECRET_FILE_DIR + file_name + ".json", "r") as file:
                self.history = json.load(file)
        except Exception as e:
            print(e)
            return False

        return True

    def soft_reset_history(self):
        """Clears the history, except for the system prompts."""
        self.history = self.history[0:2]

    def hard_reset_history(self):
        """Clears the history, system prompts set as defaults."""
        self.history = []
        self.history.append({"role": "system", "content": CONSTANT_SYSTEM_PROMPT})
        self.history.append({"role": "system", "content": SYSTEM_PROMPT})

    def total_reset_history(self):
        """Clears ALL history"""
        self.history = []

    def get_history(self) -> list:
        """Returns the history. (does not include system prompts) :)"""
        return self.history[2:]

    def get_history_list(self) -> list:
        """Returns list of all files in ./secrets/"""


if __name__ == "__main__":
    b = gpt()
    # print(b.get_text_response("tim: Hello, what is your name?"))
    print(b.get_image_response("piccture of a cat"))
