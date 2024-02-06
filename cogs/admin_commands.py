from discord import Interaction, app_commands
from discord.ext import commands
from bot import MlscBot
from pandas import read_csv
from csv import DictReader
from discord.utils import get

class AdminCommands(commands.Cog):
    def __init__(self, bot: MlscBot):
        self.bot = bot

    @app_commands.command()
    async def assign_participants_role(self, inter: Interaction):
        guild = inter.guild
        with open('Makeathon.csv', 'r') as csvfile:
            reader = DictReader(csvfile)
            for row in reader:
                for member in guild.members:
                    if str(member.id) == row["Discord Ids"]:
                        team_role = get(guild.roles, name="Participant")
                        await member.add_roles(team_role)

    @app_commands.command()
    async def serverid(self, inter: Interaction):
        await inter.response.send_message(inter.guild.id, ephemeral=True)
    
async def setup(bot: commands.Bot):
    await bot.add_cog(AdminCommands(bot))