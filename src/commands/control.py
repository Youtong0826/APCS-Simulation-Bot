from lib.cog import CogExtension
from lib.bot import Bot

from discord import (
    ButtonStyle,
    Colour,
    ComponentType,
    Embed,
    EmbedField,
    Message,
    Interaction,
    slash_command
)

from discord.ui import (
    View,
    Button,
    Select,
)

from discord.utils import find

class CommandControl(CogExtension):
    @slash_command()
    async def setting(self, ctx: Interaction):

        msg = await ctx.response.send_message(
            embed=Embed(title="設定", color=Colour.nitro_pink(), fields=[
                EmbedField(
                    "開始時間",
                    f"`{self.bot.database.get('satrt_time', '無資料')}`"
                ),
                EmbedField(
                    "通知頻道",
                    f"`{self.bot.get_channel(self.bot.database.get('notice_channel', '無資料'))}`"
                ),
                EmbedField(
                    "剩餘時間",
                    f"`{str(self.bot.get_time_left())}`"
                ),
                EmbedField(
                    "測驗連結",
                    f"`{self.bot.database.get("url")}`"
                ),
                EmbedField(
                    "身分組",
                    f"`{find(lambda x: x.id == self.bot.database.get('role'), msg.guild.roles)}`"
                )
            ]), 
            view=View(
                Button(
                    style=ButtonStyle.primary,
                    label="設定開始時間",
                    custom_id="set_time"
                ),
                Button(
                    style=ButtonStyle.success,
                    label="設定通知頻道",
                    custom_id="set_channel"
                ),
                Button(
                    style=ButtonStyle.primary,
                    label="設定測驗連結",
                    custom_id="set_url"
                ),
                Button(
                    style=ButtonStyle.success,
                    label="設定身分組",
                    custom_id="set_role"
                )
        , timeout=None))
        
        self.bot.database.set('msg', msg.id)
        self.bot.database.set('control', msg.channel_id)

    @slash_command()
    async def add_field(self, ctx: Interaction, name: str, value: str):#https://apcs-simulation.com/contest/2
        setting_channel = self.bot.get_channel(self.bot.database.get('control'))
        msg = await setting_channel.fetch_message(self.bot.database.get('msg'))

        embed = msg.embeds[0]
        embed.add_field(
            name=name,
            value=value
        )

        await msg.edit(embed=embed)
        await ctx.response.send_message('編輯成功~', ephemeral=True)

    @slash_command()
    async def notice(self, ctx: Interaction, times: int):
        notice_channel= self.bot.get_channel(self.bot.database.get('notice_channel'))
        print(notice_channel)
        embed = Embed(
            title="APCS 模擬測驗",
            url=self.bot.database.get('url'),
            description=f'`將在1小時內開始`' if times == 1 else '`將在15分鐘內開始`',
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

        role = notice_channel.guild.get_role(self.bot.database.get("role"))

        await notice_channel.send(role.mention, embed=embed)
        self.bot.database.set('sents', 9)
        
    @slash_command()
    async def add_button(self, ctx: Interaction, style: int = None, label: str = None, custom_id: str = None):
        setting_channel = self.bot.get_channel(self.bot.database.get('control'))
        msg: Message = await setting_channel.fetch_message(self.bot.database.get('msg'))
        view = View()
        for n in msg.components:
            self.bot.from_component(view, n)
        
        view.add_item(Button(
            style=ButtonStyle.success,
            label=label,
            custom_id=custom_id,
            row=1,
        ))
        
        await msg.edit(view=view)
        await ctx.response.send_message('編輯成功~', ephemeral=True)
        
    @slash_command()
    async def add_select(self, ctx: Interaction, style: int = None, label: str = None, custom_id: str = None):
        setting_channel = self.bot.get_channel(self.bot.database.get('control'))
        msg: Message = await setting_channel.fetch_message(self.bot.database.get('msg'))
        view = View()
        for n in msg.components:
            self.bot.from_component(view, n)
        
        view.add_item(Select(
            select_type=ComponentType.role_select,
            placeholder="設定測驗身分組",
            custom_id="set_role",
            row=1,
        ))
        
        await msg.edit(view=view)
        await ctx.response.send_message('編輯成功~', ephemeral=True)
        
    @slash_command()
    async def edit(self, ctx: Interaction):
        setting_channel = self.bot.get_channel(self.bot.database.get('control'))
        msg: Message = await setting_channel.fetch_message(self.bot.database.get('msg'))
        view = View()
        for n in msg.components:
            self.bot.from_component(view, n)
            
        view.remove_item(view.get_item('set_role'))
        await msg.edit(view=view)
        await ctx.response.send_message('編輯成功~', ephemeral=True)
        
    @slash_command()
    async def say(self, ctx: Interaction, *, msg: str):
        await ctx.send(msg)
        
def setup(bot: Bot):
    bot.add_cog(CommandControl(bot))