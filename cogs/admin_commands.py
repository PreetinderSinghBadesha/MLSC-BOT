from discord import Interaction, app_commands
from discord.ext import commands
from bot import MlscBot
from csv import DictReader
from discord.utils import get
import json
from google.cloud import firestore
from os import environ

# Set the environment variable for the path to your Firebase service account key JSON file
environ["GOOGLE_APPLICATION_CREDENTIALS"] = "database-key.json"

# Initialize Firestore client
db = firestore.Client()

class AdminCommands(commands.Cog):
    def __init__(self, bot: MlscBot):
        self.bot = bot

    @app_commands.command()
    async def assign_participants_role(self, inter: Interaction):
        guild = inter.guild
        member_ids_set = set(str(member.id) for member in guild.members)
        member_username_set = set(str(member.name) for member in guild.members)

        doc_ref = db.collection("Discord_Users").document("Teams")
        database_ids_set = set()

        doc = doc_ref.get()
        if doc.exists:
            discord_ids = doc.to_dict()
            for team_name, member_info in discord_ids.items():
                discord_id = member_info.get("Discord Ids")
                if discord_id:
                    database_ids_set.add(discord_id)
        else:
            print("No such document!")

        common_ids = member_ids_set.intersection(database_ids_set)
        common_names = member_username_set.intersection(database_ids_set)

        team_role = get(guild.roles, name="Participant")

        for member_id in common_ids:
            member = guild.get_member(int(member_id))
            await member.add_roles(team_role)

        for member_name in common_names:
            member = guild.get_member_named(member_name)
            await member.add_roles(team_role)

        await inter.response.send_message("Role assigned to Participants", ephemeral=True)

    @app_commands.command()
    async def serverid(self, inter: Interaction):
        await inter.response.send_message(inter.guild.id, ephemeral=True)
    
async def setup(bot: commands.Bot):
    await bot.add_cog(AdminCommands(bot))