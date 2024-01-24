import json 

with open("hidden/api_keys.json", "r") as file:
    keys = json.load(file)

gpt_api_key = keys["gpt_api_key"]
elevenlabs_api_key = keys["elevenlabs_api_key"]
discord_api_key = keys["discord_api_key"]