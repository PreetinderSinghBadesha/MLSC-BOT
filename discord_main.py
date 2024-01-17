import os
from dotenv import load_dotenv
from discord import Intents, Client, Message, Member, channel
from discord.utils import get
from discord.ext import commands
from responses import get_response
import re

load_dotenv() #to load token from somewhere safe
TOKEN:str = os.getenv('DISCORD_TOKEN')
SERVER_ID: str = 1196503338825560185

intents:Intents = Intents.default()
intents.message_content = True
client:Client = commands.Bot(command_prefix="!", intents=intents)

async def send_message(username: str, message: Message, user_message: str) -> None:
    if not user_message:
        welcome: str = f"Welcome aboard {message.author.mentiong}  !! \nWe Hope you will enjoy participating in Makeathon 6"
        await message.channel.send(welcome)
    
    if is_private := user_message[0] == '?':
        user_message = user_message[1:]
        

    if message.content.startswith("!roles"):
        await dm_about_roles(message.author)
    
    if message.content.startswith("!serverid"):
        await message.channel.send(message.channel.guild.id)

    if isinstance(message.channel, channel.DMChannel):
        await assign_roles(message)
        return

    try:
        response: str = get_response(user_message)
        await message.author.send(response) if is_private else await message.channel.send(response)
    except Exception as e:
            print(e)

@client.event
async def on_ready() -> None:
    print(f'{client.user} is now running!')

@client.event
async def assign_roles(message):
    print("Assigning roles...")

    languages = set(re.findall("python|javascript|rust|go|c\+\+|java", message.content, re.IGNORECASE))

    
    if languages:
        server = client.get_guild(SERVER_ID)
        roles = [get(server.roles, name=message.content)]
        member = await server.fetch_member(message.author.id)
    else:
        await message.channel.send("No supported languages were found in your message.")

    try:
        await member.add_roles(*roles, reason="Roles assigned by MLSC Bot.")
    except Exception as e:
        print(e)
        await message.channel.send("Error assigning roles.")  
    else:
        await message.channel.send(f"""You've been assigned the following role{"s" if len(languages) > 1 else ""} on {server.name}: { ', '.join(languages) }.""")   

@client.event
async def on_message(message: Message) -> None:
    if message.author == client.user:
        return
    
    username: str = str(message.author)
    user_message: str = message.content
    channel: str = str(message.channel)

    

    print(f'{channel} {username}: "{user_message}"')
    await send_message(username ,message, user_message)


@client.event
async def dm_about_roles(member: Member):
    print(f"DMing {member.name}...")

    await member.send(
        f"""Hi {member.name}, welcome to {member.guild.name}!

Which of these languages do you use:

* Python
* C
* JavaScript
* Rust 
* Go
* Java
* C++

Reply to this message with the language names above so I can assign you the right roles on our server.
"""
    )

def main() -> None:
     client.run(token=TOKEN)

if __name__ == '__main__':
     main()