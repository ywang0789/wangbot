import api_keys
import discord 
from discord.ext import commands
import gpt
import time

INTENTS = discord.Intents.default()
INTENTS.messages = True
INTENTS.message_content=True
BOT = commands.Bot(command_prefix='!', intents=INTENTS)

GPT = gpt.gpt()
START_TIME = time.time()
FORMATTED_START_TIME = time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime(START_TIME))
HISTORY_FILE = "history.json"

# on start
@BOT.event
async def on_ready():
    print(f'{BOT.user} has connected to Discord!')

# !hello
@BOT.command(name='hi')
async def hi_command(ctx):
    await ctx.send(f"Hi, {ctx.author.name}!")

# !wangbot
@BOT.command(name='wangbot',  help = "Talk to Wangbot.")
async def wangbot_command(ctx, *, message: str):
    message = ctx.author.name + ": " + message
    
    # get attachments if any
    if len(ctx.message.attachments) > 0:
        print(ctx.message.attachments[0].url)
        message += " " + ctx.message.attachments[0].url
    print(message)
    await ctx.send(GPT.get_text_response(message))

# !appendwang
@BOT.command(name='appendwang', help = "Appends a new system prompt.")
async def appendwang_command(ctx, *, message: str):
    GPT.append_system_prompt(message)
    await ctx.send("System prompt appened.")

# !overwritewang
@BOT.command(name='overwritewang', help = "Overwrites the system prompt.")
async def overwritewang_command(ctx, *, message: str):
    GPT.overwrite_system_prompt(message)
    await ctx.send("System prompt overwritten.")

# !session
@BOT.command(name='session', help = "Gets info about current session.")
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
        

    await ctx.send(f"""```
Start time: {FORMATTED_START_TIME}
Length: {formated_time_elapsed} seconds
This costed Wang ${money_used}
{ending_message}
```""")

# on message
@BOT.event
async def on_message(message):
    if message.author == BOT.user:
        return
    await BOT.process_commands(message)

TOKEN = api_keys.discord_token
BOT.run(TOKEN)
