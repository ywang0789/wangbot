"""
For making a gpt chatbot.
"""

import api_keys
import openai
import json
import requests
import os
import utils

API_KEY = api_keys.gpt_api_key

# language model settings
LANG_MODEL = "gpt-4-0125-preview"  # "gpt-4-0125-preview" ($0.01 / 1K tokens) OR "gpt-3.5-turbo-1106" ($0.0010 / 1K tokens)
TEXT_PRICING_RATE = 0.010 / 1000  # change if change model
HISTORY_FILE_DIR = "./secret/histories/"

# vision model settings
VISION_MODEL = "gpt-4-vision-preview"  # $0.01 / 1K tokens
VISION_PRICING_RATE = 0.010 / 1000  # change if change model


# image model settings
IMG_MODEL = "dall-e-3"  # "dall-e-3" ($0.040 / image) OR "dall-e-2 ($0.020 / image")
IMG_SIZE = "1024x1024"
IMG_PRICING_RATE = 0.020  # change if change model
IMG_QUALITY = "standard"
IMG_FILE_DIR = "./secret/images/"

# system prompts
CONSTANT_SYSTEM_PROMPT = """
You will be speaking with muliple people on a chat app, their names will be indicated in the message given to you:
<name>: <message>
Your responses do not need to follow this format.
"""

# secret system prompt
try:
    import secret.prompts as prompts

    SYSTEM_PROMPT = prompts.SYSTEM_PROMPT1  # hehe ;)
except:  # you do not have the secret sauce
    SYSTEM_PROMPT = "placeholder"


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

        # load history from default file
        self.load_history_from_default_file()

        # session usage
        self.usage = 0.00

    def get_text_response(self, user_input: str = "") -> str:
        """Returns a response from GPT. Also updates the history."""

        # input validation
        user_input_len = len(user_input)
        if user_input_len == 0:
            return "Please enter something."

        if user_input_len > 500:
            return "Please keep your input under 500 characters."

        self.history.append({"role": "user", "content": user_input})

        # get completion
        response = self.client.chat.completions.create(
            model=LANG_MODEL, messages=self.history
        )

        # extract content from completion
        response_content = response.choices[0].message.content

        # add interaction to history
        self.history.append({"role": "assistant", "content": response_content})

        # save history to default file
        self.save_history_to_default_file()

        # update session usage
        self.usage += response.usage.total_tokens * TEXT_PRICING_RATE

        return response_content

    def get_img_response(self, user_input: str):
        """Downloads and returns an image path of url response from DAll e.
        Returns False if failed."""

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
        self.usage += IMG_PRICING_RATE

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

    def get_vision_response(self, prompt: str, img_url: str) -> str:
        """Returns a response from vision (text + image). Also updates the history."""

        # format propmt
        message = {
            "role": "user",
            "content": [
                {"type": "text", "text": prompt},
                {
                    "type": "image_url",
                    "image_url": {
                        "url": img_url,
                    },
                },
            ],
        }

        # copy history into a temp var
        # IMPORTANT: bcuz vision completion and text completion are different, they have different 'messages' param formats!!!!!
        temp_history = self.history.copy()
        temp_history.append(message)

        # get completion
        response = self.client.chat.completions.create(
            model=VISION_MODEL,
            messages=temp_history,
            max_tokens=150,
        )

        # extract content from completion
        response_content = response.choices[0].message.content

        # add interaction to history
        self.history.append({"role": "user", "content": prompt + "{image}"})
        self.history.append({"role": "assistant", "content": response_content})

        # save history to default file
        self.save_history_to_default_file()

        # update session usage
        self.usage += response.usage.total_tokens * VISION_PRICING_RATE

        return response_content

    def append_system_prompt(self, new_system_prompt: str):
        """Appends a new system prompt to the history."""
        self.history.append({"role": "system", "content": new_system_prompt})

    def overwrite_system_prompt(self, new_system_prompt: str):
        """Sets the system prompt to the new system prompt."""
        self.history[0] = {"role": "system", "content": new_system_prompt}

    def get_usage(self) -> float:
        """Returns the session usage."""
        return self.usage

    def save_history_to(self, file_name: str) -> bool:
        """Saves the history to a json file.
        Returns False if failed."""
        # make dir if not exist
        if not os.path.exists(HISTORY_FILE_DIR):
            os.makedirs(HISTORY_FILE_DIR)

        file_path = os.path.join(HISTORY_FILE_DIR, f"{file_name}.json")
        try:
            with open(file_path, "w") as file:
                json.dump(self.history[2:], file)
        except:
            return False

        return True

    def load_history_from(self, file_name: str) -> bool:
        """Loads the history from a json file.
        Returns False if failed."""
        file_path = os.path.join(HISTORY_FILE_DIR, f"{file_name}.json")
        try:
            with open(file_path, "r") as file:
                # overwrite history with new history
                self.history = json.load(file)
        except:
            return False

        return True

    def save_history_to_default_file(self) -> bool:
        """Saves the history to a default file.
        Returns False if failed."""
        return self.save_history_to("default")

    def load_history_from_default_file(self) -> bool:
        """Loads the history from a default file.
        Returns False if failed."""
        return self.load_history_from("default")

    def soft_reset_history(self):
        """Clears the history, except for the system prompts."""
        self.history = self.history[0:2]

    def hard_reset_history(self):
        """Clears the history, system prompts set as defaults."""
        self.history = []
        self.history.append({"role": "system", "content": CONSTANT_SYSTEM_PROMPT})
        self.history.append({"role": "system", "content": SYSTEM_PROMPT})

    def total_reset_history(self):
        """Clears all history except the 1st system prompt."""
        self.history = self.history[0:1]

    def get_history(self) -> list:
        """Returns the history.
        (does not include system prompts) :)"""
        return self.history[2:].copy()

    def get_history_list(self) -> list:
        """Returns list of all files in history dir."""
        return os.listdir(HISTORY_FILE_DIR)

    def summarize_history(self):
        """Summarize previous parts of the conversation to reduce their size."""

        # extract and reformat converstaion from list
        conversation = ""
        for entry in self.history[2:]:  # Skip system prompts
            role = entry["role"]
            content = entry["content"]
            conversation += f"{role.capitalize()}: {content}\n"

        # generate summary
        summary_prompt = "Summarize the following conversation:\n" + conversation
        summary_response = self.client.chat.completions.create(
            model=LANG_MODEL,
            messages=[{"role": "system", "content": summary_prompt}],
        )

        # Extract summary content
        summary_content = summary_response.choices[0].message.content

        # Replace the old history with summarized
        self.history = self.history[:2]  # Keep the system prompts
        self.history.append(
            {
                "role": "system",
                "content": f"Summary of conversation so far:\n{summary_content}",
            }
        )


if __name__ == "__main__":
    import time

    b = gpt()

    # print(b.get_image_response("piccture of a cat"))
    print(
        b.get_vision_response(
            "what is this picture?",
            "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcS9-HNAsO8F1XNtS5q90_MUuGKBrU7NoFLs-g&usqp=CAU",
        )
    )
    time.sleep(10)
    print(b.get_text_response("tim: Hello, what is your name?"))

    print(b.get_text_response("john: Hello, what is my name?"))
