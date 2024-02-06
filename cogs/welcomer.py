from discord import Interaction, app_commands, Member
from discord.ext import commands
from bot import MlscBot
import json

class Welcomer(commands.Cog):
    def __init__(self, bot: MlscBot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member: Member):
        with open("./data.json", "r") as data:
            records = json.load(data)

        try:
            channel_id = records[str(member.guild.id)]
        except KeyError:
            return
        
        channel = self.bot.get_channel(int(channel_id))
        if not channel:
            return 
        
        await channel.send(f"Welcome {member.mention}!")

    
    @app_commands.command()
    async def welcome(self, inter: Interaction):
        with open("./data.json", "r") as data:
            records = json.load(data)

        records[str(inter.guild_id)] = str(inter.channel_id)
        with open("./data.json", "w") as data:
            json.dump(records, data)

        await inter.response.send_message(F"Success! {inter.channel.mention} is your Welcome Channel.")
    
async def setup(bot: commands.Bot):
    await bot.add_cog(Welcomer(bot))