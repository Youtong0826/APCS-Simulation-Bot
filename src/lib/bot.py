import os
from discord import Bot, Interaction, ApplicationContext as AppCtx
from .database import BotDatabase
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv

load_dotenv()

class Bot(Bot):
    def __init__(self, description=None, *args, **options):
        super().__init__(description, *args, **options)

        self.database_path = "bot.db"
        self.token = os.getenv("TOKEN")

    @property
    def database(self):
        return BotDatabase(self.database_path)
    
    def get_interaction_value(self, interaction: Interaction):
        return [data.get("components",{})[0].get("value") for data in interaction.data.get("components",{})]
    
    def get_select_value(self, interaction: Interaction, index: int = -1):
        return interaction.data.get("values")[index] if index != -1 else interaction.data.get("values")
    
    def is_administrator(self, ctx: AppCtx):
        return ctx.author.guild_permissions.administrator or ctx.author.get_role(1193356058694004878) or ctx.author.get_role(1193356245193723965)
    
    def get_now_time(self, time: datetime = None, hours = 8) -> datetime:
        ori = datetime.now(timezone(timedelta(hours=hours))) if not time else time
        return datetime(ori.year, ori.month, ori.day, ori.hour, ori.minute, ori.second)

    def get_time_left(self):
        time: datetime = datetime.strptime(self.database.get('start_time'), '%Y/%m/%d %H:%M:%S')
        now: datetime = self.get_now_time()
        time_left = time-now
        return time_left 
    
    def get_time_left_str(self):
        time_left = self.get_time_left()
        
        times = str(time_left).split()
        if time_left.days > 0:
            mi = times[2].split(':')
            times = f"{times[0]} 天 {mi[0]} 小時 {mi[1]} 分鐘"

        else:
            mi = times[0].split(':')
            times = f"0 天 {mi[0]} 小時 {mi[1]} 分鐘"
            
        return times
    
    def slash_command(self, **kwargs):
        return super().slash_command(**kwargs, checks=[self.is_administrator])
    
    def log(self, *text: str):
        print(self.get_now_time().strftime('[%Y/%m/%d %H:%M:%S]'), *text)