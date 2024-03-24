from lib.bot import Bot
from discord import Intents


bot = Bot(intents=Intents.all())#

@bot.event
async def on_ready():
    bot.log("I'm ready!")
    bot.log("database: \n", bot.database)

# @bot.event
# async def on_member_join(member: Member):
#     bot.log("new member join:", member.name, "id:", member.id)

if __name__ == "__main__":
    bot.load_extension("commands")
    bot.load_extension("events")
    bot.load_extension("tasks")
    bot.run(bot.token)