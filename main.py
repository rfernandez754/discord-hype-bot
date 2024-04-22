""" Main module for Discord bot """

from typing import Final
import os
from dotenv import load_dotenv
from discord import Intents
from discord.ext import commands
from responses import get_response

from dbcontroller import DBController

load_dotenv()
TOKEN: Final[str] = os.getenv('DISCORD_TOKEN')

intents = Intents.default()
intents.message_content = True
#client = Client(intents=intents)

client = commands.Bot(command_prefix='!', intents=intents)

dbcontroller = DBController()

@client.event
async def on_ready() -> None:
    """ Bot startup """

    print(f'{client.user} has started.')

@client.command()
async def add(ctx, *, arg):
    """ Function replys to user """
    await ctx.send(f"Hey there, I got your command to add: {arg}")
    await ctx.send(f"What day of the week would you like to add the reminder for {arg}?")
    print(ctx.author.name)
    print(ctx.message.content)
    print(ctx.message.created_at)
    dbcontroller.add_message_info(ctx.author.name,ctx.message.content,ctx.message.created_at)

def main() -> None:
    """ main method """

    client.run(TOKEN)


if __name__ == '__main__':
    main()
