""" main file for bot """
import api_keys
import discord
from discord.ext import commands
import gpt
import voice
import time
import secret.messages as messages

# bot setup
TOKEN = api_keys.discord_token
INTENTS = discord.Intents.default()
INTENTS.messages = True
INTENTS.message_content = True
BOT = commands.Bot(command_prefix="!", intents=INTENTS, help_command=None)

# gpt setup
GPT = gpt.gpt()
START_TIME = time.time()
FORMATTED_START_TIME = time.strftime(
    "%a, %d %b %Y %H:%M:%S", time.localtime(START_TIME)
)

# messages
WARNING_MESSAGE = messages.WARNING_MESSAGE
ATTACK_MESSAGE = messages.ATTACK_MESSAGE


# on start
@BOT.event
async def on_ready():
    """Prints when bot is ready."""
    print(f"{BOT.user} has connected to Discord!")


# on message
@BOT.event
async def on_message(message):
    if message.author == BOT.user:
        return
    await BOT.process_commands(message)


#############COMMANDS#################
# !help
@BOT.command(name="help")
async def help(ctx):
    # Main commands
    main_embed = discord.Embed(
        title="Main commands",
        description="List of available commands:",
        color=0x00FF00,
    )
    main_embed.add_field(name="!hi", value="Says hi to message author.", inline=False)
    main_embed.add_field(
        name="!wangbot <message>",
        value="Get text response from Wangbot GPT.",
        inline=False,
    )
    main_embed.add_field(
        name="!wangpic <message>",
        value="Generate image from a prompt.",
        inline=False,
    )
    main_embed.add_field(
        name="!wangspeak <message>",
        value="Generate voice from a prompt.",
        inline=False,
    )
    main_embed.add_field(
        name="!atkwang",
        value="Print attack Wang message.",
        inline=False,
    )
    main_embed.add_field(
        name="!warnwang",
        value="Print warn Wang message.",
        inline=False,
    )
    main_embed.add_field(
        name="!wanginfo",
        value="Gets info about current session.",
        inline=False,
    )

    await ctx.send(embed=main_embed)

    # Config commands
    config_embed = discord.Embed(title="Config commands", description="Configuring commands for WangBot" ,color=0xFF0000)
    main_embed.add_field(
        name="!showwang",
        value="Shows the current history (does not include system prompts).",
        inline=False,
    )
    config_embed.add_field(
        name="!appendwang <message>",
        value="Appends a new system prompt <message> to end of history.",
        inline=False,
    )
    config_embed.add_field(
        name="!overwritewang <message>",
        value="Overwrites the system prompt with <message>.",
        inline=False,
    )

    config_embed.add_field(
        name="!savewang <file_name>",
        value="Saves current history to <file_name>.json.",
        inline=False,
    )
    config_embed.add_field(
        name="!loadwang <file_name>",
        value="Loads the history from <file_name>.json.",
        inline=False,
    )
    config_embed.add_field(
        name="!softresetwang",
        value="Resets the history but keeps initial system prompts untouched\.",
        inline=False,
    )
    config_embed.add_field(
        name="!hardresetwang",
        value="Resets the history and sets system prompt to default.",
        inline=False,
    )
    await ctx.send(embed=config_embed)
    


# !hello
@BOT.command(name="hi")
async def hi_command(ctx):
    """Says hi to message author."""
    print(f"{ctx.message.created_at}:{ctx.author.name}: !hi.")
    await ctx.send(f"Hi, {ctx.author.name}!")

# !wangbot
@BOT.command(name="wangbot")
async def wangbot_command(ctx, *, message: str):
    """Get text response from Wangbot GPT."""
    print(f"{ctx.message.created_at}:{ctx.author.name}: !wangbot {message}")
    message = ctx.author.name + ": " + message
    await ctx.send(GPT.get_text_response(message))


# !wangpic
@BOT.command(name="wangpic")
async def wangimg_command(ctx, *, message: str):
    """Generate image from a prompt."""
    print(f"{ctx.message.created_at}:{ctx.author.name}: !wangpic {message}")
    await ctx.send(GPT.get_image_response(message))

# !wangspeak
@BOT.command(name="wangspeak")
async def wangspeak_command(ctx, *, message: str):
    """Generate voice from a prompt."""
    print(f"{ctx.message.created_at}:{ctx.author.name}: !wangspeak {message}")

    #validate message
    if len(message) == 0:
        await ctx.send("Please enter a message.")
        return

    if not voice.get_speech(message):
        await ctx.send("Could not generate speech.")

    await ctx.send(file=discord.File(voice.AUDIO_FILE_NAME))

# !wanginfo
@BOT.command(name="wanginfo")
async def usage_command(ctx):
    """Gets info about current session."""
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

# !showwang
@BOT.command(name="showwang")
async def show_command(ctx):
    """Shows the current history (does not include system prompts)."""
    print(f"{ctx.message.created_at}:{ctx.author.name}: !showwang.")

    if len(GPT.get_history()) == 0:
        await ctx.send("History is empty.")
        return

    formatted_history = ""
    for message in GPT.get_history():
        formatted_history += f"{message['role']}: {message['content']}\n"
    await ctx.send(formatted_history)


# !appendwang
@BOT.command(name="appendwang")
async def appendwang_command(ctx, *, message: str):
    """Appends a new system prompt to end of history."""
    print(f"{ctx.message.created_at}:{ctx.author.name}: !appendwang {message}")
    GPT.append_system_prompt(message)
    await ctx.send("System prompt appened.")


# !overwritewang
@BOT.command(name="overwritewang")
async def overwritewang_command(ctx, *, message: str):
    """Overwrites the system prompt with message."""
    print(f"{ctx.message.created_at}:{ctx.author.name}: !overwritewang {message}")
    GPT.overwrite_system_prompt(message)
    await ctx.send("System prompt overwritten.")


# !savewang
@BOT.command(name="savewang")
async def save_command(ctx, *, file_name):
    """Saves current history to a json file name."""
    print(f"{ctx.message.created_at}:{ctx.author.name}: !save {file_name}")

    # check if file name is valid
    if len(file_name) == 0 or len(file_name) > 10:
        await ctx.send("Please enter new file name.")
        return

    # save history
    if not GPT.save_history_to(file_name):
        await ctx.send(f"Could not save history to {file_name}.json.")
        return

    await ctx.send(f"History saved to {file_name}.json.")


# !loadwang
@BOT.command(name="loadwang")
async def load_command(ctx, *, file_name):
    """Loads the history from a json file name."""
    print(f"{ctx.message.created_at}:{ctx.author.name}: !load {file_name}")

    # check if file name is valid
    if len(file_name) == 0 or len(file_name) > 10:
        await ctx.send("Please enter a new file name.")
        return

    # load history
    if not GPT.load_history_from(file_name):
        await ctx.send(f"Could not load history from {file_name}.json.")
        return

    await ctx.send(f"History loaded from {file_name}.json.")


# !softresetwang
@BOT.command(name="softresetwang")
async def softreset_command(ctx):
    """Resets the history (keeps initial system prompt)."""
    print(f"{ctx.message.created_at}:{ctx.author.name}: !softreset.")
    GPT.soft_reset_history()
    await ctx.send("History has been reset softly.")


# !hardresetwang
@BOT.command(name="hardresetwang")
async def hardreset_command(ctx):
    """Resets the history (sets system prompt to default)."""
    print(f"{ctx.message.created_at}:{ctx.author.name}: !hardreset.")
    GPT.hard_reset_history()
    await ctx.send("History has been reset hardly.")


# !atkwang
@BOT.command(name="atkwang")
async def atkwang_command(ctx):
    print(f"{ctx.message.created_at}:{ctx.author.name}: !atkwang.")
    await ctx.send(ATTACK_MESSAGE)


# !warnwang
@BOT.command(name="warnwang")
async def warnwang_command(ctx):
    print(f"{ctx.message.created_at}:{ctx.author.name}: !warnwang.")
    await ctx.send(WARNING_MESSAGE)


BOT.run(TOKEN)
