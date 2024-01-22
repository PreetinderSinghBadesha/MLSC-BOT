from discord import Interaction, app_commands
from discord.ext import commands
from bot import MlscBot

class AdminCommands(commands.Cog):
    def __init__(self, bot: MlscBot):
        self.bot = bot

    @app_commands.command()
    async def serverid(self, inter: Interaction):
        await inter.response.send_message(inter.guild.id, ephemeral=True)
    
async def setup(bot: commands.Bot):
    await bot.add_cog(AdminCommands(bot))