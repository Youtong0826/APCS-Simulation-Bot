from lib.bot import Bot

from discord import (
    Intents,
    Embed,
    Colour,
    Member,
    TextChannel,
    Interaction,
    ComponentType as CT,
)

from discord.ui import (
    View,
    Modal,
    Button,
    Select,
    InputText
)

bot = Bot(intents=Intents.all())#

@bot.slash_command(checks=[bot.is_administrator])
async def setting(ctx: Interaction):
    embed = Embed(title="設定", color=Colour.nitro_pink())

    embed.add_field(
        name="開始時間",
        value=f"`{bot.database.get('time', '無資料')}`",
    )

    embed.add_field(
        name="通知頻道",
        value=f"`{bot.get_channel(int(bot.database.get('channel', '無資料')))}`",
    )

    embed.add_field(
        name="剩餘時間",
        value=f"`{str(bot.get_time_left())}`"
    )

    set_time = Button(style=1, label="設定開始時間", custom_id="set_time")
    set_channel = Button(style=3, label="設定通知頻道", custom_id="set_channel")
    
    msg = await ctx.response.send_message(embed=embed, view=View(set_time, set_channel))
    bot.database.set('msg', msg.id)
    bot.database.set('control', msg.channel_id)

@bot.event
async def on_ready():
    bot.log("I'm ready!")
    bot.log("database: \n", bot.database)

@bot.event
async def on_member_join(member: Member):
    bot.log("new member join:", member.name, "id:", member.id)

@bot.event
async def on_interaction(interaction: Interaction):
    if interaction.is_command():
        return await setting(interaction)
    
    custom_id = interaction.custom_id
    if custom_id == "set_time":
        return await interaction.response.send_modal(
            Modal(
                InputText(label="日期與時間", placeholder="年/月/日 時:分:秒"), 
                title="設定開始日期與時間", 
                custom_id="set_time_modal"
            )
        )
        
    elif custom_id == "set_channel":
        return await interaction.response.send_message("請點選以下選單來設定頻道", 
            view=View(
                Select(
                    CT.channel_select, 
                    placeholder="選擇要通知的頻道", 
                    custom_id="set_channel_select"
                ),
                timeout=None
            ), 
            ephemeral=True
        )
    
    elif custom_id == "set_time_modal":
        data: list[str] = bot.get_interaction_value(interaction)
        try:
            bot.database.set("time", data[0])
            return await interaction.response.send_message(f"設定成功! 資料:`{data[0]}`", ephemeral=True)

        except Exception as ex:
            bot.log(ex)
            return await interaction.response.send_message(f"設定失敗! 詳情:\n```{ex}```", ephemeral=True)
        
    elif custom_id == "set_channel_select":
        channel: TextChannel = bot.get_channel(int(bot.get_select_value(interaction, 0)))
        try:
            bot.database.set("notice_channel", channel.id)
            return await interaction.response.send_message(f"設定成功! 頻道:`{channel.name}` (id: `{channel.id}`)", ephemeral=True)
        except Exception as ex:
            bot.log(ex)
            return await interaction.response.send_message(f"設定失敗! 詳情:\n```{ex}```", ephemeral=True)

if __name__ == "__main__":
    bot.load_extension("task")
    bot.run(bot.token)