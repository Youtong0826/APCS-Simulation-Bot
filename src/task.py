from discord.ext import tasks, commands
from discord.utils import find
from lib.bot import Bot 

class Task(commands.Cog):
    def __init__(self, bot: Bot):
        self.bot = bot
        self.refresh.start()
        
    @property
    def times(self):
        return self.bot.get_time_left()

    @tasks.loop(minutes=5.0)
    async def refresh(self):
        #notice_channel = await self.bot.get_channel(self.bot.database.get('channel'))
        show_channel = self.bot.get_channel(self.bot.database.get('time_left_channel'))
        setting_channel = self.bot.get_channel(self.bot.database.get('control'))
        msg = await setting_channel.fetch_message(self.bot.database.get('msg'))
        
        embed = msg.embeds[0]
        embed.fields[0].value = f"`{self.bot.database.get('time', '無資料')}`"
        embed.fields[1].value = f"`{self.bot.get_channel(self.bot.database.get('notice_channel'))}`"
        embed.fields[2].value = f"`{self.times}`"
        await msg.edit(embed=embed)
        await show_channel.edit(name=self.times)
        
        self.bot.log(f"updated the channel name & message ! ({self.times})")
        
    @refresh.before_loop
    async def before_loop(self):
        self.bot.log("task is waiting...")
        await self.bot.wait_until_ready()

def setup(bot: Bot):
    bot.add_cog(Task(bot))