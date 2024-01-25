""" This file contains the API keys """
import json 

with open("hidden/keys.json", "r") as file:
    keys = json.load(file)

gpt_api_key = keys["gpt_api_key"]
elevenlabs_api_key = keys["elevenlabs_api_key"]
discord_public_key = keys["discord_public_key"]
discord_app_id = keys["discord_app_id"]
discord_token = keys["discord_token"]
