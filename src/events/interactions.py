from lib.classes import CogExtension
from lib.bot import Bot

from discord import (
    Cog,
    TextChannel,
    Interaction,
    ComponentType as CT,
)

from discord.ui import (
    View,
    Modal,
    Select,
    InputText
)

class EventInteraction(CogExtension):
    @Cog.listener
    async def on_interaction(self, interaction: Interaction):
    
        if interaction.is_command():
            #print(interaction.data)
            return await self.bot.get_command(interaction.data['name'])(interaction)
            #return await setting(interaction)

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
            data: list[str] = self.bot.get_interaction_value(interaction)
            try:
                self.bot.database.set("start_time", data[0])
                self.bot.database.set('sents', 1)
                return await interaction.response.send_message(f"設定成功! 資料:`{data[0]}`", ephemeral=True)

            except Exception as ex:
                self.bot.log(ex)
                return await interaction.response.send_message(f"設定失敗! 詳情:\n```{ex}```", ephemeral=True)

        elif custom_id == "set_channel_select":
            channel: TextChannel = self.bot.get_channel(int(self.bot.get_select_value(interaction, 0)))
            try:
                self.bot.database.set("notice_channel", channel.id)

                return await interaction.response.send_message(f"設定成功! 頻道:`{channel.name}` (id: `{channel.id}`)", ephemeral=True)
            except Exception as ex:
                self.bot.log(ex)
                return await interaction.response.send_message(f"設定失敗! 詳情:\n```{ex}```", ephemeral=True)
            
def setup(bot: Bot):
    bot.add_cog(EventInteraction(bot))