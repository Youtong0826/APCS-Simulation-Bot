from discord.ext import tasks, commands
from discord import Embed, Colour
from lib.bot import Bot 

class Task(commands.Cog):
    def __init__(self, bot: Bot):
        self.bot = bot
        self.refresh_ch.start()
        self.refresh_msg.start()
        self.notice.start()
        self.is_sent = 0
        
    @property
    def times(self):
        return self.bot.get_time_left()
    
    @property
    def times_str(self):
        return self.bot.get_time_left_str()
    
    @property
    def sents(self):
        return self.bot.database.get('sents', 1)

    @tasks.loop(minutes=1.0)
    async def notice(self):
        if (self.times != "無資料" and self.times.days <= 0 and ((self.times.seconds <= 3600 and self.sents == 1) or (self.times.seconds <= 900 and self.sents == 2))):
            notice_channel= self.bot.get_channel(self.bot.database.get('notice_channel'))
            
            embed = Embed(
                title="APCS 模擬測驗",
                url=self.bot.database.get('url'),
                description=f'`將在1小時內開始`' if self.sents == 1 else '`將在15分鐘內開始`',
                color=Colour.yellow()
            )
            
            embed.add_field(
                name='開始時間',
                value=f'`{self.bot.database.get("start_time")}`'
            )
            
            embed.add_field(
                name="競賽時長",
                value='`0 天 2 小時 30 分鐘`'
            )
            
            role = notice_channel.guild.get_role(1199703262320939028)
            
            await notice_channel.send(role.mention, embed=embed)
            self.bot.database.add('sents', 1)
    
    @tasks.loop(minutes=5.0)
    async def refresh_ch(self):
        show_channel = self.bot.get_channel(self.bot.database.get('time_left_channel'))
        await show_channel.edit(name=self.times_str)
        
        self.bot.log(f"updated the channel name ({self.times_str})")
        
    @tasks.loop(minutes=10.0)
    async def refresh_msg(self):
        #notice_channel = await self.bot.get_channel(self.bot.database.get('channel'))
        setting_channel = self.bot.get_channel(self.bot.database.get('control'))
        msg = await setting_channel.fetch_message(self.bot.database.get('msg'))
        
        embed = msg.embeds[0]
        embed.fields[0].value = f"`{self.bot.database.get('start_time', '無資料')}`"
        embed.fields[1].value = f"`{self.bot.get_channel(self.bot.database.get('notice_channel'))}`"
        embed.fields[2].value = f"`{self.times_str}`"
        
        await msg.edit(embed=embed)
        
        self.bot.log(f"updated the message ({self.times_str})")
        
    @refresh_ch.before_loop
    @refresh_msg.before_loop
    async def before_loop(self):
        self.bot.log(f"task is waiting...")
        await self.bot.wait_until_ready()

def setup(bot: Bot):
    bot.add_cog(Task(bot))