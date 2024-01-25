"""
For making a gpt chatbot.
"""
import openai
import api_keys
import hidden.prompts
import json
import time

API_KEY = api_keys.gpt_api_key

MODEL = "gpt-4-turbo-preview"
PRICING_RATE = 0.01/1000  # $0.01 per 1000 tokens, change if change model


CONSTANT_SYSTEM_PROMPT = """
You will be speaking with muliple people, their names will be indicated in the message.
the format is:
<name>: <message>
Your responses do not need to follow this format.

"""

SYSTEM_PROMPT = hidden.prompts.SYSTEM_PROMPT1 # hehe ;)


class gpt:
    """A class that create a gpt that chats and stuff"""
    def __init__(self):
        # set api key
        openai.api_key = API_KEY

        # init history for saving context 
        self.history = []
        # set system prompt to history
        self.history.append({"role": "system", "content": CONSTANT_SYSTEM_PROMPT})
        self.history.append({"role": "system", "content": SYSTEM_PROMPT})

        # session usage
        self.token_usage = 0

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
        response = openai.chat.completions.create(model=MODEL, messages=self.history)
        # extract content from completion
        response_content = response.choices[0].message.content

        # add response to history
        self.history.append({"role": "assistant", "content": response_content})

        # update session usage
        self.token_usage += response.usage.total_tokens

        return response_content
    
    def append_system_prompt(self, new_system_prompt: str):
        """Appends a new system prompt to the history."""
        self.history.append({"role": "assistant", "content": new_system_prompt})
        
        return "System prompt appended."
    
    def overwrite_system_prompt(self, new_system_prompt: str):
        """Sets the system prompt to the new system prompt."""
        self.history[0] = {"role": "system", "content": new_system_prompt}

        print(self.history)
        
        return "system prompt overwritten."
    
    def get_money_usage(self):
        """Returns the session usage."""
        return self.token_usage * PRICING_RATE
    
    def save_history(self, file_name: str = "history.json"):
        """Saves the history to a json file."""
        with open(file_name, "w") as file:
            json.dump(self.history, file)

    def load_history(self, file_name: str = "history.json"):
        """Loads the history from a json file."""
        with open(file_name, "r") as file:
            self.history = json.load(file)
    
if __name__ == "__main__":
    b = gpt()
    print(b.get_text_response("tim: Hello, what is your name?"))
    b.save_history()