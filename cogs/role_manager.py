from discord import Interaction, app_commands, Member
from discord.utils import get
from discord.ext import commands
from bot import MlscBot
from re import findall, IGNORECASE

class RoleManager(commands.Cog):
    def __init__(self, bot: MlscBot):
        self.bot = bot

    @app_commands.command()
    async def view_roles(self, inter: Interaction, member:Member):
        print(f"Viewing Roles to {member.name} .....")

        await inter.response.send_message(f""""Hi {member.name}, welcome to {member.guild.name}!

Which of these languages do you use:

* Python (🐍)
* JavaScript (🕸️)
* Rust (🦀)
* Go (🐹)
* C++ (🐉)

To Assign yourself Roles Memtioned above use /assign_role command

Example: /assign_role Python
                    OR
         /assign_role Python Go
""", ephemeral=True)
    
    @app_commands.command()
    async def assign_role(self, inter: Interaction, member:Member, givenroles: str):
        print("Assigning roles...")

        requestedRoles = set(findall("python|javascript|rust|go|c\+\+", givenroles, IGNORECASE))
        if requestedRoles:
            server = inter.guild
            print(f"before: {server.roles}")
            roles = [get(server.roles, name="Go")]
            
            # member = await server.fetch_member(message.author.id)

            try:
                print(roles)
                await member.add_roles(*roles, reason="Roles assigned by MlscBot.")
            except Exception as e:
                print(e)
                await inter.response.send_message("Error assigning roles.", ephemeral=True)
            else:
                await inter.response.send_message(f"""You've been assigned the following role{"s" if len(requestedRoles) > 1 else ""} on {server.name}: { ', '.join(requestedRoles) }.""", ephemeral=True)
        
        else:
            await inter.response.send_message("No supported Roles were found in your message.", ephemeral=True)
    
async def setup(bot: commands.Bot):
    await bot.add_cog(RoleManager(bot))