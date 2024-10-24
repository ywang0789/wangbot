import discord
from discord.ext import commands

from assistant import Assistant
from dall_e import DallE
from social_credit import CreditManager

# DEV_GUILD = discord.Object(id=1199749859050270750)
# DEV_CHANNEL_ID = 1295035228255027281

# PROD_GUILD = discord.Object(id=1094705369797898380)
# PROD_SOCIAL_CREDIT_CHANNEL_ID = 1230908894080012298

GUILD = discord.Object(id=1094705369797898380)
GUILD_DEV = discord.Object(id=1199749859050270750)

CHANNEL_ID = 1230908894080012298


class WangBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.messages = True
        intents.message_content = True
        intents.members = True
        super().__init__(command_prefix="!", intents=intents, help_command=None)

        # social credit manager
        self._credit_manager = CreditManager()

        # DallE image gen
        self._dalle = DallE()

        # assistant
        self._assistant = Assistant()

        # COMMANDS
        @self.tree.command(name="wangbot", description="Talk to wangbot", guild=GUILD)
        async def _get_wangbot_response(
            interaction: discord.Interaction, message: str
        ) -> None:
            """Get response from gpt assistant"""
            user = interaction.user.display_name
            file_path = None
            response_message = None
            try:
                await interaction.response.defer()

                response = self._assistant.get_reponse(user, message)
                response_message = response.get("response")
                file_path = response.get("file_path")

            except Exception as e:
                response_message = f"Failed to get response: {e}"

            if file_path is not None:
                await interaction.followup.send(
                    response_message, files=[discord.File(file_path)]
                )
            else:
                await interaction.followup.send(response_message)

        @self.tree.command(
            name="wangpic",
            description="Generates an image with prompt",
            guild=GUILD,
        )
        async def _generate_image(
            interaction: discord.Interaction, prompt: str
        ) -> None:
            try:
                await interaction.response.defer()

                image_path = self._dalle.generate_image(prompt)
                await interaction.followup.send(
                    "Here:", files=[discord.File(image_path)]
                )
            except Exception as e:
                await interaction.followup.send(f"Coud not generate image: {e}")

        @self.tree.command(
            name="get_credit",
            description="Get a user's social credit score",
            guild=GUILD,
        )
        async def _get_credit(interaction: discord.Interaction, user: str) -> None:
            try:
                await interaction.response.defer()

                if user:
                    reply = self._credit_manager.get_user_score(user)

            except Exception as e:
                reply = f"Failed to get score: {e}"

            embed = discord.Embed(
                title="Social Credit Score", description=reply, color=0xFF0000
            )

            await interaction.followup.send(embed=embed)

        @self.tree.command(
            name="get_credit_history",
            description="Get a user's social credit score history",
            guild=GUILD,
        )
        async def _get_history(interaction: discord.Interaction, user: str) -> None:
            try:
                await interaction.response.defer()

                if user:
                    reply = self._credit_manager.get_formated_user_history(user)

            except Exception as e:
                reply = f"Failed to get history: {e}"

            embed = discord.Embed(
                title="Social Credit History", description=reply, color=0xFF0000
            )

            await interaction.followup.send(embed=embed)

        @self.tree.command(
            name="get_credit_all",
            description="Get all users' social credit scores",
            guild=GUILD,
        )
        async def _get_all_credit_scores(interaction: discord.Interaction) -> None:
            try:
                await interaction.response.defer()

                reply = self._credit_manager.get_formated_all_scores()

            except Exception as e:
                reply = f"Failed to get scores: {e}"

            embed = discord.Embed(
                title="Social Credit Scores", description=reply, color=0xFF0000
            )

            await interaction.followup.send(embed=embed)

    async def on_ready(self) -> None:
        print(f"{self.user} has connected!")
        # sync commands with server
        try:
            synced = await self.tree.sync(guild=GUILD)
            synced_dev = await self.tree.sync(guild=GUILD_DEV)
            print(f"Synced {len(synced)} commands to prod")
            print(f"Synced {len(synced_dev)} commands to dev")
        except Exception as e:
            print(f"Failed to sync: {e}")

    async def on_message(self, message) -> None:
        if message.author == self.user:
            return

        if message.channel.id == CHANNEL_ID:
            content = message.content.strip().lower()
            if content.startswith("+") or content.startswith("-"):
                try:
                    reply = self._credit_manager.process_transaction_message(content)

                except Exception as e:
                    reply = f"Failed to process transaction: {e}"

                embed = discord.Embed(
                    title="Social Credit Update", description=reply, color=0xFF0000
                )

                await message.channel.send(embed=embed)
