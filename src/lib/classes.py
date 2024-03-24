from .bot import Bot
import discord

class CogExtension(discord.Cog):
    def __init__(self, bot: Bot):
        self.bot = bot