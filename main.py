from discord import Client, Intents, Message
from dotenv import load_dotenv
import os
from response import get_response

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")

intents: Intents = Intents.default()
intents.message_content = True

client: Client = Client(intents= intents)

@client.event
async def send_message(message: Message, user_message:str) ->None:

    # To cheack if message from user is empty or not
    if not user_message:
        print("It is Empty message")

    # To check if it is private message or not
    if is_private := user_message[0] == '?':  
        user_message = user_message[1: ]

    try:
        response: str = get_response(user_message)

        # If private then message will we send to user privately otherwise on channel
        await message.author.send(response) if is_private else await message.channel.send(response)

    except Exception as e:
        print(e)

@client.event
async def on_ready() -> None:
    print(f'{client.user} is now Running Baby !!')

@client.event
async def on_message(message: Message):
    # For stopping bot from messaging itself
    if message.author == client.user:
        return
    
    username: str = str(message.author)
    user_message: str = message.content
    channel: str = str(message.channel)

    print(f'[{channel} ({username}) : "{user_message}"]')

    await send_message(message, user_message)
    
if __name__ == "__main__":
    client.run(token= TOKEN)