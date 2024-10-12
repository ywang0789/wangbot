import discord
from discord.ext import commands

from dall_e import DallE

DEV_GUILD = discord.Object(id=1199749859050270750)  # ID of server to sync commands


class WangBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.messages = True
        intents.message_content = True
        intents.members = True
        super().__init__(command_prefix="!", intents=intents, help_command=None)

        # DallE image gen
        self.dalle = DallE()

        # COMMANDS
        @self.tree.command(name="hi", description="Says hello", guild=DEV_GUILD)
        async def say_hello(interaction: discord.Interaction):
            await interaction.response.send_message(
                f"Hello, {interaction.user.display_name}!"
            )

        @self.tree.command(
            name="wangpic",
            description="Generates an image with prompt",
            guild=DEV_GUILD,
        )
        async def generate_image(interaction: discord.Interaction, prompt: str):
            try:
                await interaction.response.defer()

                image_path = self.dalle.get_img_response(prompt)
                await interaction.followup.send(
                    "Here:", files=[discord.File(image_path)]
                )
            except Exception as e:
                await interaction.followup.send(f"Coud not generate image: {e}")

    async def on_ready(self) -> None:
        print(f"{self.user} has connected!")
        # sync commands with server
        try:
            synced = await self.tree.sync(guild=DEV_GUILD)
            print(f"Synced {len(synced)} commands")
        except Exception as e:
            print(f"Failed to sync: {e}")

    async def on_message(self, message) -> None:
        if message.author == self.user:
            return
