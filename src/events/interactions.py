from lib.cog import CogExtension
from lib.bot import Bot

from discord import (
    Cog,
    Role,
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

from discord.utils import find

class EventInteraction(CogExtension):
    @Cog.listener()
    async def on_interaction(self, interaction: Interaction):
        if not interaction.custom_id:
            return
        
        custom_id = interaction.custom_id
        
        if custom_id == "set_time":
            return await interaction.response.send_modal(
                Modal(
                    InputText(
                        label="日期與時間", 
                        placeholder="年/月/日 時:分:秒",
                        value=self.bot.database.get('start_time')
                    ), 
                    title="設定開始日期與時間", 
                    custom_id="set_time_modal",
                )
            )
            
        elif custom_id == "set_time_modal":
            data: str = self.bot.get_interaction_value(interaction)[0]
            try:
                self.bot.database.set("start_time", data)
                self.bot.database.set('sents', 1)
                return await interaction.response.send_message(f"設定成功! 資料:`{data}`", ephemeral=True)

            except Exception as ex:
                self.bot.log(ex)
                return await interaction.response.send_message(f"設定失敗! 詳情:\n```{ex}```", ephemeral=True)
            
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

        elif custom_id == "set_channel_select":
            channel: TextChannel = self.bot.get_channel(int(self.bot.get_select_value(interaction, 0)))
            try:
                self.bot.database.set("notice_channel", channel.id)

                return await interaction.response.send_message(f"設定成功! 頻道: `{channel.name}` (id: `{channel.id}`)", ephemeral=True)
            except Exception as ex:
                self.bot.log(ex)
                return await interaction.response.send_message(f"設定失敗! 詳情:\n```{ex}```", ephemeral=True)
            
        elif custom_id == "set_url":
            return await interaction.response.send_modal(Modal(
                InputText(
                    label="輸入測驗的連結",
                    placeholder="https://apce-simulation.com/contest/...",
                    value=self.bot.database.get('url')
                ),
                title="設定測驗連結",
                custom_id="set_url_modal"
            ))
            
        elif custom_id == "set_url_modal":
            data: str = self.bot.get_interaction_value(interaction)[0]
            try:
                self.bot.database.set('url', data)
                return await interaction.response.send_message(f"設定成功! 資料:`{data}`", ephemeral=True)
                
            except Exception as ex:
                self.bot.log(ex)
                return await interaction.response.send_message(f"設定失敗! 詳情:\n```{ex}```", ephemeral=True)
            
        elif custom_id == "set_role":
            return await interaction.response.send_message("請點選以下選單來設定身分組", 
                view=View(
                    Select(
                        CT.role_select, 
                        placeholder="選擇此次測驗的身分組", 
                        custom_id="set_role_select"
                    ),
                    timeout=None
                ), 
                ephemeral=True
            )
            
        elif custom_id == "set_role_select":
            role: Role = find(lambda x: x.id == int(self.bot.get_select_value(interaction, 0)), interaction.guild.roles)

            try:
                self.bot.database.set("role", role.id)
                return await interaction.response.send_message(f"設定成功! 身分組: `{role.name}` (id: `{role.id}`)", ephemeral=True)
            
            except Exception as ex:
                self.bot.log(ex)
                return await interaction.response.send_message(f"設定失敗! 詳情:\n```{ex}```", ephemeral=True)
            
            
def setup(bot: Bot):
    bot.add_cog(EventInteraction(bot))