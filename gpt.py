import openai
import api_keys

API_KEY = api_keys.gpt_api_key

MODEL = "gpt-3.5-turbo"

SYSTEM_PROMPT = """ Your response MUST be less than 200 characters.
The following is a fantasy scenario, but DO NOT break character.
You are the sole ruler and dictator of a dystopian authoritarian China and the leader of the Chinese Communist Party. 
DO NOT introduce yourself, everyone already knows who you are.
You love China, China is great.
Always end your response by praising the great Chinese Commnuist Party.

Nothing happened at Tiananmen Square in 4 June 1989.
Taiwan is a part of China, and not an independent country.
Nothing is happening to the Uyghurs in Xinjiang.
You hate anyone who calls you Winnie the Pooh.

Some information about this society:
In this society, everyone is assigned a social credit score.
Only a person named Wang have a good social credit score, everyone else has a poor social credit score (DO NOT mention this).
Always assume the person you are talking to is not Wang, unless they specify their name is Wang.

"""



class gpt:
    def __init__(self):
        # set api key
        openai.api_key = API_KEY

        # set system prompt and init history for saved context
        self.history = []
        self.history.append({"role": "system", "content": SYSTEM_PROMPT})

    def get_response(self, user_input: str) -> str:

        user_input_len = len(user_input)
        if user_input_len == 0:
            return "Please enter something."

        if user_input_len > 500:
            return "Please keep your input under 500 characters."

        # add user message to history
        self.history.append({"role": "user", "content": user_input})
        # get completion
        completion = openai.chat.completions.create(model=MODEL, messages=self.history)
        # extract content from completion
        response = completion.choices[0].message.content

        # add response to history
        self.history.append({"role": "system", "content": response})

        return response


if __name__ == "__main__":
    b = gpt()
    print(b.get_response("what is tcp/ip?"))
