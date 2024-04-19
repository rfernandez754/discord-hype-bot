""" Main module for Discord bot """

from typing import Final
import os
from dotenv import load_dotenv
from discord import Intents, Client
from responses import get_response

load_dotenv()
TOKEN: Final[str] = os.getenv('DISCORD_TOKEN')

intents = Intents.default()
intents.message_content = True
client = Client(intents=intents)

async def send_message(message, user_message) -> None:
    """ Sends a message to the discord channel """

    if not user_message:
        print("Empty message.")
        return

    response = get_response(user_message)
    await message.channel.send(response)

@client.event
async def on_ready() -> None:
    """ Bot startup """

    print(f'{client.user} has started.')


@client.event
async def on_message(message) -> None:
    """ Handles the incoming message from discord users """

    if message.author == client.user:
        return

    username = str(message.author)
    user_message = message.content
    channel = str(message.channel)

    print(f'[{channel}] {username}: "{user_message}"')
    await send_message(message, user_message)

def main() -> None:
    """ main method """

    client.run(TOKEN)


if __name__ == '__main__':
    main()
