from lib.classes import CogExtension
from lib.bot import Bot

from discord import (
    Cog,
    Member
)

class EventMembers(CogExtension):
    @Cog.listener()
    async def on_member_join(self, member: Member):
        self.bot.log("new member join:", member.name, "id:", member.id)
        
def setup(bot: Bot):
    bot.add_cog(EventMembers(bot))