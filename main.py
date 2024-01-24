import os
import api_keys
import discord 
from discord.ext import commands
import gpt

TOKEN = api_keys.discord_token

intents=discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='$', intents = intents)
gptbot = gpt.gpt(api_keys.gpt_api_key)

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')

# @bot.command(name='wanggpt')
# # async def wanggpt(ctx, *, arg):
# #     print("WHO CALLED ME?!")
    
# #     await ctx.send(reply)

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if message.content.startswith('$wanggpt'):
        substr = message.content.split('$wanggpt', 1)
        prompt = substr[1]
        print("prompt: " + prompt)
        reply = gptbot.get_response(prompt)
        print("reply: " + reply)
        await message.channel.send(reply)




bot.run(TOKEN)
