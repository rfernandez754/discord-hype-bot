""" Main module for Discord bot """

import os
from typing import Final
from dotenv import load_dotenv
from discord import Intents
from discord.ext import commands
# from responses import get_response
from dbcontroller import DBController

class DiscordBot(commands.Bot):
    """ Class for handling Dicord Bot startup and execution """
    def __init__(self):
        intents = Intents.default()
        intents.message_content = True
        super().__init__(command_prefix='!', intents=intents)
        self.db_controller = DBController()
        self.load_cogs()

    async def on_ready(self) -> None:
        """ Bot startup """
        print(f'{self.user} has started.')

    def load_cogs(self):
        """ Load cogs into the bot. Current working directory must be within the main Discord Reminder Bot Folder. """
        for filename in os.listdir("./cogs"):
            if filename.endswith(".py") and filename != "__init__.py":
                self.load_extension(f'cogs.{filename[:-3]}')
                print(f'cogs.{filename[:-3]}')

def main() -> None:
    """ main method """
    load_dotenv()
    token: Final[str] = os.getenv('DISCORD_TOKEN')
    bot = DiscordBot()
    bot.run(token)

if __name__ == '__main__':
    main()
