""" main file for bot """
import api_keys
import discord
from discord.ext import commands
import gpt
import time

# bot setup
TOKEN = api_keys.discord_token
INTENTS = discord.Intents.default()
INTENTS.messages = True
INTENTS.message_content = True
BOT = commands.Bot(command_prefix="!", intents=INTENTS)

# gpt setup
GPT = gpt.gpt()
START_TIME = time.time()
FORMATTED_START_TIME = time.strftime(
    "%a, %d %b %Y %H:%M:%S", time.localtime(START_TIME)
)
HISTORY_FILE_DIR = "./hidden/"


# on start
@BOT.event
async def on_ready():
    print(f"{BOT.user} has connected to Discord!")


# !hello
@BOT.command(name="hi")
async def hi_command(ctx):
    await ctx.send(f"Hi, {ctx.author.name}!")


# !wangbot
@BOT.command(name="wangbot", help="Talk to Wangbot.")
async def wangbot_command(ctx, *, message: str):
    message = ctx.author.name + ": " + message

    await ctx.send(GPT.get_text_response(message))


# !appendwang
@BOT.command(name="appendwang", help="Appends a new system prompt.")
async def appendwang_command(ctx, *, message: str):
    GPT.append_system_prompt(message)
    await ctx.send("System prompt appened.")


# !overwritewang
@BOT.command(name="overwritewang", help="Overwrites the system prompt.")
async def overwritewang_command(ctx, *, message: str):
    GPT.overwrite_system_prompt(message)
    await ctx.send("System prompt overwritten.")


# !session
@BOT.command(name="session", help="Gets info about current session.")
async def usage_command(ctx):
    # calculate time elapsed
    time_elapsed = time.time() - START_TIME
    formated_time_elapsed = time.strftime("%H:%M:%S", time.gmtime(time_elapsed))

    # ending text
    money_used = GPT.get_money_usage()
    ending_message = ""
    if money_used == 0:
        ending_message = "Thank you for saving Wang's money."
    elif money_used <= 0.1:
        ending_message = "Is this the best you can do?"
    elif money_used <= 0.5:
        ending_message = "Not bad."
    elif money_used <= 1:
        ending_message = "Wang might financially recover from this."
    elif money_used > 1:
        ending_message = "Wang is in shambles."

    await ctx.send(
        f"""```
Start time: {FORMATTED_START_TIME}
Length: {formated_time_elapsed} seconds
This costed Wang ${money_used}
{ending_message}
```"""
    )


# !save
@BOT.command(name="save", help="Saves the history to a json file.")
async def save_command(ctx, *, file_name):
    # check if file name is valid
    if len(file_name) == 0:
        await ctx.send("Please enter a file name.")
        return
    # format file name
    file_name = HISTORY_FILE_DIR + file_name + ".json"
    # save history
    if not GPT.save_history(file_name):
        await ctx.send(f"Could not save history to {file_name}.")
        return
    

    await ctx.send(f"History saved to {file_name}.")


# !load
@BOT.command(name="load", help="Loads the history from a json file.")
async def load_command(ctx, *, file_name):
    # check if file name is valid
    if len(file_name) == 0:
        await ctx.send("Please enter a file name.")
        return
    # format file name
    file_name = HISTORY_FILE_DIR + file_name + ".json"

    # load history
    if not GPT.load_history(file_name):
        await ctx.send(f"Could not load history from {file_name}.")
        return

    await ctx.send(f"History loaded from {file_name}.")


# on message
@BOT.event
async def on_message(message):
    if message.author == BOT.user:
        return
    await BOT.process_commands(message)


BOT.run(TOKEN)
