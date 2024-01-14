import discord

class CogExtension(discord.Cog):
    def __init__(self, bot: discord.Bot):
        self.bot = bot