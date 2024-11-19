import logging.config
from lib.bot import Bot
from discord import Intents

import logging

logger = logging.getLogger("bot")
logger.setLevel(logging.INFO)

bot = Bot(intents=Intents.all())#

@bot.event
async def on_ready():
    bot.log("I'm ready!")
    bot.log("database:", bot.database)

if __name__ == "__main__":
    bot.load_extension("commands")
    bot.load_extension("events")
    bot.load_extension("tasks")
    bot.run(bot.token)