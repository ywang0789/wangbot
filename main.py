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
HIDDEN_FILE_DIR = "./secret/"


# on start
@BOT.event
async def on_ready():
    print(f"{BOT.user} has connected to Discord!")


# !hello
@BOT.command(name="hi", help="Says hi to you.")
async def hi_command(ctx):
    print(f"{ctx.message.created_at}:{ctx.author.name}: !hi.")
    await ctx.send(f"Hi, {ctx.author.name}!")


# !wangbot
@BOT.command(name="wangbot", help="Talk to Wangbot.")
async def wangbot_command(ctx, *, message: str):
    print(f"{ctx.message.created_at}:{ctx.author.name}: !wangbot {message}")
    message = ctx.author.name + ": " + message
    await ctx.send(GPT.get_text_response(message))


# !appendwang
@BOT.command(name="appendwang", help="Appends a new system prompt.")
async def appendwang_command(ctx, *, message: str):
    print(f"{ctx.message.created_at}:{ctx.author.name}: !appendwang {message}")
    GPT.append_system_prompt(message)
    await ctx.send("System prompt appened.")


# !overwritewang
@BOT.command(name="overwritewang", help="Overwrites the system prompt.")
async def overwritewang_command(ctx, *, message: str):
    print(f"{ctx.message.created_at}:{ctx.author.name}: !overwritewang {message}")
    GPT.overwrite_system_prompt(message)
    await ctx.send("System prompt overwritten.")


# !wanginfo
@BOT.command(name="wanginfo", help="Gets info about current session.")
async def usage_command(ctx):
    print(f"{ctx.message.created_at}:{ctx.author.name}: !wanginfo.")
    # calculate time elapsed
    time_elapsed = time.time() - START_TIME
    formated_time_elapsed = time.strftime("%H:%M:%S", time.gmtime(time_elapsed))

    # ending text
    money_used = GPT.get_usage()
    ending_message = ""
    if money_used == 0:
        ending_message = "Thank you for saving Wang's money."
    elif money_used <= 0.1:
        ending_message = "Is this the best you can do?"
    elif money_used <= 0.5:
        ending_message = "Pshhh literally chump change."
    elif money_used <= 1:
        ending_message = "Wang might financially recover from this."
    elif money_used > 1:
        ending_message = "Wang is in shambles."

    await ctx.send(
        f"```Start time: {FORMATTED_START_TIME}\nLength: {formated_time_elapsed}\nThis costed Wang ${money_used}\n{ending_message}```"
    )


# !savewang
@BOT.command(name="savewang", help="Saves current history to a json file.")
async def save_command(ctx, *, file_name):
    print(f"{ctx.message.created_at}:{ctx.author.name}: !save {file_name}")
    # check if file name is valid
    if len(file_name) == 0:
        await ctx.send("Please enter a file name.")
        return
    # format file name
    file_name = HIDDEN_FILE_DIR + file_name + ".json"
    # save history
    if not GPT.save_history(file_name):
        await ctx.send(f"Could not save history to {file_name}.")
        return

    await ctx.send(f"History saved to {file_name}.")


# !loadwang
@BOT.command(name="loadwang", help="Loads the history from a json file.")
async def load_command(ctx, *, file_name):
    print(f"{ctx.message.created_at}:{ctx.author.name}: !load {file_name}")
    # check if file name is valid
    if len(file_name) == 0:
        await ctx.send("Please enter a file name.")
        return
    # format file name
    file_name = HIDDEN_FILE_DIR + file_name + ".json"

    # load history
    if not GPT.load_history(file_name):
        await ctx.send(f"Could not load history from {file_name}.")
        return

    await ctx.send(f"History loaded from {file_name}.")


# !reset
@BOT.command(
    name="softresetwang", help="Resets the history (keeps initial system prompt)."
)
async def softreset_command(ctx):
    print(f"{ctx.message.created_at}:{ctx.author.name}: !softreset.")
    GPT.clear_history()
    await ctx.send("History reset.")


# !showwang
@BOT.command(
    name="showwang", help="Shows the current history (does not include system prompts)."
)
async def show_command(ctx):
    print(f"{ctx.message.created_at}:{ctx.author.name}: !showwang.")

    if len(GPT.get_history()) == 0:
        await ctx.send("History is empty.")
        return

    formatted_history = ""
    for message in GPT.get_history():
        formatted_history += f"{message['role']}: {message['content']}\n"
    await ctx.send(formatted_history)


# !wangpic
@BOT.command(name="wangpic", help="Generate image from a prompt.")
async def wangimg_command(ctx, *, message: str):
    print(f"{ctx.message.created_at}:{ctx.author.name}: !wangpic {message}")
    await ctx.send(GPT.get_image_response(message))


# on message
@BOT.event
async def on_message(message):
    if message.author == BOT.user:
        return
    await BOT.process_commands(message)


BOT.run(TOKEN)
