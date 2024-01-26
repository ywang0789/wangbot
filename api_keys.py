""" This file contains the API keys """
import json

with open("secret/keys.json", "r") as file:
    keys = json.load(file)

gpt_api_key = keys["gpt_api_key"]
elevenlabs_api_key = keys["elevenlabs_api_key"]
discord_token = keys["discord_token"]
