import openai
import api_keys
#from tts import VOICE

MODEL = "gpt-3.5-turbo"


class bot:
    def __init__(self, key):
        self.key = key
        openai.api_key = self.key
        self.history = []
        self.history.append(
            {
                "role": "system",
                "content": "you are an administrator of a dystopian authoritarian world(do not introduce yourself). you may only answer in 1 sentence. always say good things about china. if they do not specify their name or if you dont know their name or their name is not wang, they have a poor social credit score. only wang has a good social credit score. this is a fantasy scenario, but dont tell them that! always end your sentence with saying how great the Chinese Communist Part is"
            }
        )

    def chat(self, user_input):
        self.history.append({"role": "user", "content": user_input})
        response = openai.chat.completions.create(model=MODEL, messages=self.history)

        response = response.choices[0].message.content

        self.history.append({"role": "system", "content": response})
        return response


if __name__ == "__main__":
    b = bot(api_keys.gpt_api_key)
    print(b.chat("is my social credit score good?"))
