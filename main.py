""" main file for bot """

import api_keys
import discord
from discord.ext import commands
import gpt
import voice
import datetime
import re


# bot setup
TOKEN = api_keys.discord_token
INTENTS = discord.Intents.default()
INTENTS.messages = True
INTENTS.message_content = True
INTENTS.members = True
BOT = commands.Bot(command_prefix="!", intents=INTENTS, help_command=None)

# gpt setup
GPT = gpt.gpt()
START_TIME = datetime.datetime.now().timestamp()
FORMATTED_START_TIME = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


# messages
try:
    import secret.messages as secret_messages

    WARNING_MESSAGE = secret_messages.WARNING_MESSAGE
    ATTACK_MESSAGE = secret_messages.ATTACK_MESSAGE
except Exception as e:
    print("Thou dost not have secret sauce.")
    WARNING_MESSAGE = "placeholder"
    ATTACK_MESSAGE = "placeholder"


# on start
@BOT.event
async def on_ready():
    """Prints when bot is ready."""
    print(f"{BOT.user} has connected to Discord!")


# on member join
@BOT.event
async def on_member_join(member):
    """Welcomes new members to the server."""
    # try to find a channel named 'general' in the server
    general_channel = discord.utils.get(member.guild.text_channels, name="general")
    if general_channel:  # if channel is found
        gpt_message = (
            member.display_name + ": " + "Hello, I have just joined the server!"
        )
        response = GPT.get_text_response(gpt_message)
        await general_channel.send(response)
    else:  # if channel is not found
        print(f"Could not find general channel in {member.guild.name}.")


# on message
@BOT.event
async def on_message(message):
    """Responds to messages and process commands."""

    # ignore self
    if message.author == BOT.user:
        return

    # Check if the message is a reply to the bot
    """ responds when the bot is replied to"""
    if message.reference is not None and message.reference.resolved:
        replied_message = message.reference.resolved
        if replied_message.author == BOT.user:
            print(
                f"{message.created_at}:{message.author.name}: reply: {message.content}"
            )
            gpt_message = (
                message.author.display_name + ": " + message.content
            )  # format message for prompt
            response = GPT.get_text_response(gpt_message)
            await message.channel.send(response)
            return

    # # BOT is mentioned
    # """ responses when the bot is mentioned """
    # if BOT.user.mentioned_in(message):
    #     print(f"{message.created_at}:{message.author.name}: mention: {message.content}")
    #     gpt_message = (
    #         message.author.display_name + ": " + message.content
    #     )  # format message for prompt
    #     response = GPT.get_text_response(gpt_message)
    #     await message.channel.send(response)
    #     return

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
        value="Generate image from a prompt. (Now uploads the img instead of sending url)",
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
    config_embed = discord.Embed(
        title="Config commands",
        description="Configuring commands for WangBot",
        color=0xFF0000,
    )
    config_embed.add_field(
        name="!showwang <file_name>",
        value="Sends the indicated json history file.",
        inline=False,
    )

    config_embed.add_field(
        name="!showwanglist",
        value="Shows list of available histories to load.",
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
    config_embed.add_field(
        name="!removewang",
        value="Removes all system prompts.",
        inline=False,
    )
    config_embed.add_field(
        name="!summarizewang",
        value="Summarizes the history. (The entire history is passed into chat completion every prompt. So this is to keep the history from getting too long.)",
        inline=False,
    )
    await ctx.send(embed=config_embed)


# !hello
@BOT.command(name="hi")
async def hi_command(ctx):
    """Says hi to message author."""
    print(f"{ctx.message.created_at}:{ctx.author.name}: !hi.")
    await ctx.send(f"Hi, {ctx.author.display_name}!")


# !wangbot
@BOT.command(name="wangbot")
async def wangbot_command(ctx, *, message: str):
    """Get text response from Wangbot GPT."""
    print(f"{ctx.message.created_at}:{ctx.author.name}: !wangbot {message}")

    # check if message has attachments
    if len(ctx.message.attachments) > 1:
        await ctx.send("Please only attach one image.")
    elif len(ctx.message.attachments) == 1:  # message with one attachment

        # get attachment url
        url = ctx.message.attachments[0].url

        # format message for GPT prompt and history (no need for real url)
        message = ctx.author.display_name + ": " + message + " {some image url}"

        try:
            response = GPT.get_vision_response(message, url)
            await ctx.send(response)
        except:
            await ctx.send("Could not get image response.")

    else:  # all text message

        # parse message for urls

        # Regex stuff ..... IDK REGEX DONT @ ME ¯\_(ツ)_/¯###########
        url_pattern = r"http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+"
        # Regex makes me go blind ....##############################

        urls = re.findall(url_pattern, message)
        message = re.sub(
            url_pattern, "{some url}", message
        )  # replace urls with {some url}
        # format message for GPT prompt and history
        message = ctx.author.display_name + ": " + message
        if len(urls) > 1:  # message with multiple urls
            await ctx.send("Please only include one url.")
        elif len(urls) == 1:  # message with one url
            try:
                response = GPT.get_vision_response(message, urls[0])
                await ctx.send(response)
            except:
                await ctx.send("Could not get image response.")
        else:  # message with no urls
            try:
                response = GPT.get_text_response(message)
                await ctx.send(response)
            except:
                await ctx.send("Could not get text response.")


# !wangpic
@BOT.command(name="wangpic")
async def wangimg_command(ctx, *, message: str):
    """Generate image from a prompt. Sends the file path to the image."""
    print(f"{ctx.message.created_at}:{ctx.author.name}: !wangpic {message}")

    try:
        file_path = GPT.get_img_response(message)
        await ctx.send(file=discord.File(file_path))
    except:
        await ctx.send("Could not generate image.")


# !wangspeak
@BOT.command(name="wangspeak")
async def wangspeak_command(ctx, *, message: str = ""):
    """Generate voice from a prompt."""
    print(f"{ctx.message.created_at}:{ctx.author.name}: !wangspeak {message}")

    # validate message
    if len(message) == 0:
        await ctx.send("Please enter a message.")
        return

    try:
        file_path = voice.get_speech(message)
        await ctx.send(file=discord.File(file_path))
    except:
        await ctx.send("Could not generate speech.")


# !wanginfo
@BOT.command(name="wanginfo")
async def usage_command(ctx):
    """Gets info about current session."""
    print(f"{ctx.message.created_at}:{ctx.author.name}: !wanginfo.")
    # calculate time elapsed
    time_elapsed = datetime.datetime.now().timestamp() - START_TIME
    formated_time_elapsed = str(datetime.timedelta(seconds=time_elapsed))

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


##################CONFIG####################################
# !removewang
@BOT.command(name="removewang")
async def friendlywang_command(ctx):
    """Remove all system prompts.(except first one)"""
    print(f"{ctx.message.created_at}:{ctx.author.name}: !removewang.")
    GPT.total_reset_history()
    await ctx.send("Goodbye")


# showwanglist
@BOT.command(name="showwanglist")
async def showanglist_command(ctx):
    """Shows list of available histories to load."""
    print(f"{ctx.message.created_at}:{ctx.author.name}: !showanglist.")

    embed = discord.Embed(
        title="Available histories",
        description="List of available histories:",
    )
    for history in GPT.get_history_list():
        embed.add_field(name=history, value=" ", inline=False)

    await ctx.send(embed=embed)


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


# !showwang
@BOT.command(name="showwang")
async def show_command(ctx, *, file_name: str = ""):
    """Sends the indicated json history file."""
    print(f"{ctx.message.created_at}:{ctx.author.name}: !showwang {file_name}")

    # check if file name is valid
    if len(file_name) == 0 or len(file_name) > 10:
        await ctx.send("Please enter a new file name (< 10 chars).")
        return

    # send history
    try:
        file_path = GPT.get_history_file_path(file_name)
        await ctx.send(file=discord.File(file_path))
    except:
        await ctx.send(f"Could not send {file_name}.json.")


# !savewang
@BOT.command(name="savewang")
async def save_command(ctx, *, file_name: str = ""):
    """Saves current history to a json file name."""
    print(f"{ctx.message.created_at}:{ctx.author.name}: !savewang {file_name}")

    # check if file name is valid
    if len(file_name) == 0 or len(file_name) > 10:
        await ctx.send("Please enter new file name (< 10 chars).")
        return

    # save history
    try:
        GPT.save_history_to(file_name)
    except:
        await ctx.send(f"Could not save history to {file_name}.json.")

    await ctx.send(f"History saved to {file_name}.json.")


# !loadwang
@BOT.command(name="loadwang")
async def load_command(ctx, *, file_name: str = ""):
    """Loads the history from a json file name."""
    print(f"{ctx.message.created_at}:{ctx.author.name}: !loadwang {file_name}")

    # check if file name is valid
    if len(file_name) == 0 or len(file_name) > 10:
        await ctx.send("Please enter a new file name (< 10 chars).")
        return

    # load history
    try:
        GPT.load_history_from(file_name)
    except:
        await ctx.send(f"Could not load history from {file_name}.json.")

    await ctx.send(f"History loaded from {file_name}.json.")


# !softresetwang
@BOT.command(name="softresetwang")
async def softreset_command(ctx):
    """Resets the history (keeps initial system prompt)."""
    print(f"{ctx.message.created_at}:{ctx.author.name}: !softresetwang")
    GPT.soft_reset_history()
    await ctx.send("History has been reset softly.")


# !hardresetwang
@BOT.command(name="hardresetwang")
async def hardreset_command(ctx):
    """Resets the history (sets system prompt to default)."""
    print(f"{ctx.message.created_at}:{ctx.author.name}: !hardresetwang")
    GPT.hard_reset_history()
    await ctx.send("History has been reset hardly.")


# !atkwang
@BOT.command(name="atkwang")
async def atkwang_command(ctx):
    print(f"{ctx.message.created_at}:{ctx.author.name}: !atkwang")
    await ctx.send(ATTACK_MESSAGE)


# !warnwang
@BOT.command(name="warnwang")
async def warnwang_command(ctx):
    print(f"{ctx.message.created_at}:{ctx.author.name}: !warnwang")
    await ctx.send(WARNING_MESSAGE)


# !summarizewang
@BOT.command(name="summarizewang")
async def summarizewang_command(ctx):
    print(f"{ctx.message.created_at}:{ctx.author.name}: !summarizewang")
    GPT.summarize_history()
    await ctx.send("History summarized.")


BOT.run(TOKEN)
