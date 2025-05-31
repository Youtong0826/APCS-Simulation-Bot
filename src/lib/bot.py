import os
from typing import (
    Any,
    Union,
)

from datetime import (
    datetime, 
    timedelta, 
    timezone
)

from discord import (
    Bot, 
    ActionRow,
    SelectMenu,
    Interaction, 
    ComponentType,
    Button as DiscordButton,
    ApplicationContext as AppCtx
)

from discord.ui import (
    View,
    Button,
    Select
)

from .database import BotDatabase
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
    
    def get_select_value(self, interaction: Interaction, index: int = -1) -> Union[Any, list[Any]]:
        return interaction.data.get("values")[index] if index != -1 else interaction.data.get("values")
    
    def from_component(self, view: View, component: Union[ActionRow, DiscordButton, SelectMenu]):
        kwargs = component.to_dict()
        kwargs.pop('type')
        
        match component.type:
            case ComponentType.button:
                view.add_item(Button(**kwargs))
                
            case ComponentType.select:
                view.add_item(Select(**kwargs))
                
            case ComponentType.role_select:
                view.add_item(Select(select_type=ComponentType.role_select, **kwargs))
                
            case ComponentType.user_select:
                view.add_item(Select(select_type=ComponentType.user_select, **kwargs))
                
            case ComponentType.channel_select:
                view.add_item(Select(select_type=ComponentType.channel_select, **kwargs))
                
            case _:
                for c in component.children:
                    self.from_component(view, c)

    @staticmethod                
    def is_administrator(ctx: AppCtx):
        return ctx.author.guild_permissions.administrator or ctx.author.get_role(1193356058694004878) or ctx.author.get_role(1193356245193723965)
    
    @staticmethod
    def is_manager(ctx: AppCtx):
        return ctx.author.id == 856041155341975582         \
    		or ctx.author.get_role(1193356058694004878)    \
        	or ctx.author.get_role(1193356245193723965)    \
            or ctx.author.get_role(1193361341411496007)    \
    
    def get_now_time(self, time: datetime = None, hours = 8) -> datetime:
        ori = datetime.now(timezone(timedelta(hours=hours))) if not time else time
        return datetime(ori.year, ori.month, ori.day, ori.hour, ori.minute, ori.second)

    def get_time_left(self):
        time: datetime = datetime.strptime(self.database.get('start_time'), '%Y/%m/%d %H:%M:%S')
        now: datetime = self.get_now_time()
        time_left = time-now
        return time_left if now < time else "無資料"
    
    def get_time_left_str(self):
        time_left = self.get_time_left()
        
        if time_left == "無資料":
            return time_left
        
        times = str(time_left).split()
        if time_left.days > 0:
            mi = times[2].split(':')
            times = f"{times[0]} 天 {mi[0]} 小時 {mi[1]} 分鐘"

        else:
            mi = times[0].split(':')
            times = f"0 天 {mi[0]} 小時 {mi[1]} 分鐘"
            
        return times
    
    def slash_command(self, **kwargs):
        return super().slash_command(**kwargs, checks=[self.is_manager])

    def load_extension(self, folder: str, mode: str = "load", is_notice: bool = True) -> None:

        loading_method = {
            "load":super().load_extension,
            "reload":super().reload_extension,
            "unload":super().unload_extension
        }

        if is_notice:
            print(f"start {mode}ing {folder}")

        for Filename in os.listdir(f'src/{folder}'):
            if Filename.endswith(".py"):
                loading_method[mode](f"{folder}.{Filename[:-3]}")
                if is_notice:
                    print(f'-- {mode}ed "{Filename}"')

        print(f"{mode}ing {folder} end")
    
    def log(self, *text: str, sep: str = None):
        print(self.get_now_time().strftime('[%Y/%m/%d %H:%M:%S]'), *text, sep=sep)