from discord import Interaction, app_commands, PermissionOverwrite, Color, Member, Forbidden, Button, ButtonStyle, SelectOption, Embed
from discord.utils import get
from discord.ext import commands
from bot import MlscBot
from discord.ui import View, Select, button


members_that_need_teams = {
            "Appdev" : ["Preet", "Josh", "King"],
            "Webdev" : ["Mudit", "Sham", "Tim"],
            "Design" : ["Name 1", "Name 2", "Name 3"],
            "ML/AI" : ["Bro 1", "Bro 2", "Bro 3"],
            "Backend" : ["Lol 1", "Lol 2", "Lol 3"],
            }

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
                await guild.create_role(name=f"Team {team_name}", colour=Color.from_rgb(0, 31, 63))
                print(f"{author.name} Created role 'Team {team_name}'")
                team_role = get(guild.roles, name=f"Team {team_name}")
                admin = get(guild.roles, name=f"Team {team_name}")

                print(team_role)
                
                #Assign team leader and team role to command excuter
                await author.add_roles(team_role)
                await author.add_roles(team_leader)

                overwrites[team_role] = PermissionOverwrite(connect=True)

                #Create voice channel for team
                team_voice_channel = await guild.create_voice_channel(name=f"{team_name}'s Voice channel", overwrites=overwrites)
                print(f"{author.name} created {team_voice_channel.name} channel for team {team_name} .....")
                await inter.response.send_message(f"{team_name}'s Voice channel Created", ephemeral=True)

            except Exception as e:
                print(e)
                await inter.response.send_message("You don't have permission to create teams.")

        else:
            inter.response.send_message("Enter team name", ephemeral=True) 

    @app_commands.command()
    async def join_team_member(self, inter: Interaction, team_name: str, member: Member):
        author = inter.user
        guild = inter.guild
        team_leader = get(guild.roles, name="Team Leader")
        role_to_assign = get(guild.roles, name=f"Team {team_name}")

        button_prompt = ButtonPrompt(team_name=team_name)

        if role_to_assign in author.roles and team_leader in author.roles:
            try:
                await inter.response.send_message(f"Invitation send to {member.mention}")
                await member.send(f"Do you want to join team {team_name}.", view=button_prompt)
                await button_prompt.wait()

                #when invite is accepted
                if button_prompt.value == True:
                    await member.add_roles(role_to_assign)
                    await member.send(f"You have accepted invitation from Team {team_name}.")
                    await author.send(f"{member.mention} have accepted your invitation to {team_name}.")

                #when invite is rejected
                elif button_prompt.value == False:
                    await member.send(f"You have rejected invitation from Team {team_name}.")
                    await author.send(f"{member.mention} have rejected your invitation to {team_name}.")
                    
            except Forbidden:
                await inter.response.send_message(f"{author.mention} don't have the permissions to assign roles.", ephemeral=True)

        else:
            await inter.response.send_message(f"{author.mention} can't use teamname of other teams", ephemeral=True)

    @app_commands.command()
    async def find_team(self, inter: Interaction):
        dropdown = TeamDropdown()
        view = DropdownView(dropdown)
        
        try:
            await inter.response.send_message("Select your interest:", view=view, ephemeral=True)
        
        except IndexError:
            print("list Index error is happening ....")
        
    @app_commands.command()
    async def find_member(self, inter: Interaction):
        dropdown = MemberDropdown()
        view = DropdownView(dropdown)

        try:
            await inter.response.send_message("Select your Member dev:", view=view, ephemeral=True)
        
        except IndexError:
            print("list Index error is happening ....")


class ButtonPrompt(View):
    def __init__(self, team_name:str):
        super().__init__(timeout=60)
        self.value = None
        self.team_name = team_name

    #Invitation Accept button
    @button(label="Yes", style=ButtonStyle.success)
    async def yes(self, inter: Interaction, button: Button):
        self.value = True
        button.disabled = True
        await inter.response.defer()
        self.stop()

    #Invitation Rejection button
    @button(label="No", style=ButtonStyle.danger)
    async def no(self, inter:Interaction, button: Button):
        self.value = False
        button.disabled = True
        await inter.response.defer()
        self.stop()

class MemberDropdown(Select):
    def __init__(self):
        options = {
            SelectOption(
                label="App dev", description="description", emoji="📱", value="Appdev"
            ),
            SelectOption(
                label="Web Dev", description="description", emoji="🕸️", value="Webdev"
            ),
            SelectOption(
                label="ML/Ai", description="description", emoji="🤖", value="ML/AI"
            ),
            SelectOption(
                label="Design", description="description", emoji="🖼️", value="Design"
            ),
            SelectOption(
                label="Backend", description="description", emoji="⚙️", value="Backend"
            ),
        }

        super().__init__(placeholder="Select :", options=options)
    
    async def callback(self, inter: Interaction):
        member_list_embed = Embed(title="Members for available", color=0x00FFB3)
        member_list = members_that_need_teams[self.values[0]]
        for member in member_list:
            member_list_embed.add_field(name=member, value="Value", inline=False)

        await inter.response.send_message(embed=member_list_embed)

class TeamDropdown(Select):
    def __init__(self):
        options = {
            SelectOption(
                label="App dev", description="description", emoji="📱", value="Appdev"
            ),
            SelectOption(
                label="Web Dev", description="description", emoji="🕸️", value="Webdev"
            ),
            SelectOption(
                label="ML/Ai", description="description", emoji="🤖", value="ML/AI"
            ),
            SelectOption(
                label="Design", description="description", emoji="🖼️", value="Design"
            ),
            SelectOption(
                label="Backend", description="description", emoji="⚙️", value="Backend"
            ),
        }

        super().__init__(placeholder="Select :", options=options)
    
    async def callback(self, inter: Interaction): 
        members_that_need_teams[self.values[0]].append("Name")
        print(members_that_need_teams[self.values[0]])
        await inter.response.send_message(f"You have selected {self.values[0]}", ephemeral=True)

class DropdownView(View):
    def __init__(self, dropdown: Select):
        super().__init__(timeout=60)
        self.add_item(dropdown) 


async def setup(bot: commands.Bot):
    await bot.add_cog(TeamManager(bot))