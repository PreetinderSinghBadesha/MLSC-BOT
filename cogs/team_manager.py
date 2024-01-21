from discord import Interaction, app_commands, PermissionOverwrite, Color, Member
from discord.utils import get
from discord.ext import commands
from bot import MlscBot

class TeamManager(commands.Cog):
    def __init__(self, bot: MlscBot):
        self.bot = bot

    @app_commands.command()
    async def create_team(self, inter:Interaction, team_name: str):
        guild = inter.guild
        author = inter.user
        team_leader = get(guild.roles, name="Team Leader")

        # Create overwrites with allowed roles
        overwrites = {
            guild.default_role: PermissionOverwrite(connect=False),
            author: PermissionOverwrite(connect=True, manage_channels=True)
        }
        
        if team_name:
            try:
                #Create role for team
                await guild.create_role(name=f"{team_name} Team", colour=Color.from_rgb(0, 31, 63))
                print(f"{author.name} Created role '{team_name} Team'")
                team_role = get(guild.roles, name=f"{team_name} Team")

                print(team_role)
                
                #Assign team leader and team role to command excuter
                await author.add_roles(team_role)
                await author.add_roles(team_leader)

                #Create voice channel for team
                overwrites[team_role] = PermissionOverwrite(connect=True)
                team_voice_channel = await guild.create_voice_channel(name=f"{team_name}'s Voice channel", overwrites=overwrites)
                print(f"{author.name} created {team_voice_channel.name} channel for team {team_name} .....")
                await inter.response.send_message(f"{team_name}'s Voice channel Created", ephemeral=True)

            except Exception as e:
                print(e)

        else:
            inter.response.send_message("Enter team name", ephemeral=True)     

    @app_commands.command()
    async def delete_team(self, inter: Interaction, team_name: str):
        if team_name:
            try:
                team_voice_channel = f"{team_name}'s Voice channel"
                for channel in inter.channel.guild.channels:
                    if channel.name == team_voice_channel:
                        channel.delete()
                print(f"{inter.user.name} Deleted {team_voice_channel} channel for team {team_name} .....")
                await inter.response.send_message(f"{team_name}'s Voice channel Deleted", ephemeral=True)
            
            except Exception as e:
                print(e)
        else:
            inter.response.send_message("Enter team name", ephemeral=True)

async def setup(bot: commands.Bot):
    await bot.add_cog(TeamManager(bot))