from lib.classes import CogExtension
from lib.bot import Bot

from discord import (
    Embed,
    Colour,
    Message,
    Interaction,
    ButtonStyle,
    ComponentType,
    slash_command
)

from discord.ui import (
    View,
    Button,
    Select,
    role_select,
)

class CommandControl(CogExtension):
    @slash_command()
    async def setting(self, ctx: Interaction):
        embed = Embed(title="設定", color=Colour.nitro_pink())

        embed.add_field(
            name="開始時間",
            value=f"`{self.bot.database.get('satrt_time', '無資料')}`",
        )

        embed.add_field(
            name="通知頻道",
            value=f"`{self.bot.get_channel(int(self.bot.database.get('channel', '無資料')))}`",
        )

        embed.add_field(
            name="剩餘時間",
            value=f"`{str(self.bot.get_time_left())}`"
        )

        set_time = Button(style=1, label="設定開始時間", custom_id="set_time")
        set_channel = Button(style=3, label="設定通知頻道", custom_id="set_channel")

        msg = await ctx.response.send_message(embed=embed, view=View(set_time, set_channel))
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
    async def test(self, ctx: Interaction):
        notice_channel= self.bot.get_channel(1193484208077819974)
        print(notice_channel)
        embed = Embed(
            title="APCS 模擬測驗",
            url=self.bot.database.get('url'),
            description='`將在10分鐘內開始`',
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

        role = notice_channel.guild.get_role(1196288338576035880)

        await notice_channel.send(role.mention, embed=embed)
        self.bot.database.add('sents', 1)
        
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
        
def setup(bot: Bot):
    bot.add_cog(CommandControl(bot))