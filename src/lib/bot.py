import os
from typing import (
    Any,
    Union,
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

from database import Database
from lib.timing import get_now_time
from dotenv import load_dotenv

load_dotenv()

class Bot(Bot):
    def __init__(self, description=None, *args, **options):
        super().__init__(description, *args, **options)

        self.database_path = "src/bot.db"
        self.token = os.getenv("TOKEN")

    @property
    def database(self):
        return Database(self.database_path)
    
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
                    
    def is_administrator(self, ctx: AppCtx):
        return ctx.author.guild_permissions.administrator or ctx.author.get_role(1193356058694004878) or ctx.author.get_role(1193356245193723965)
    
    def is_manager(self, ctx: AppCtx):
        return ctx.author.id == 856041155341975582
    
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
        print(get_now_time().strftime('[%Y/%m/%d %H:%M:%S]'), *text, sep=sep)