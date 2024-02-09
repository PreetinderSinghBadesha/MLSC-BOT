from discord import Interaction, app_commands
from discord.ext import commands
from bot import MlscBot
from csv import DictReader
from discord.utils import get

class AdminCommands(commands.Cog):
    def __init__(self, bot: MlscBot):
        self.bot = bot

    @app_commands.command()
    async def assign_participants_role(self, inter: Interaction):
        guild = inter.guild
        member_ids_set = set(str(member.id) for member in guild.members)

        with open('Makeathon.csv', 'r') as csvfile:
            reader = DictReader(csvfile)
            csv_ids_set = set(row["Discord Ids"] for row in reader)

        common_ids = member_ids_set.intersection(csv_ids_set)

        team_role = get(guild.roles, name="Participant")

        for member_id in common_ids:
            member = guild.get_member(int(member_id))
            await member.add_roles(team_role)

        await inter.response.send_message("Role assigned to Participants", ephemeral=True)

    @app_commands.command()
    async def serverid(self, inter: Interaction):
        await inter.response.send_message(inter.guild.id, ephemeral=True)
    
async def setup(bot: commands.Bot):
    await bot.add_cog(AdminCommands(bot))