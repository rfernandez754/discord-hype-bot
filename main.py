""" Main module for Discord bot """

import os
from typing import Final
from dotenv import load_dotenv
from discord import Intents
from discord.ext import commands
from dbcontroller import DBController

class MyHelpCommand(commands.HelpCommand):
    """ Custome help command implementation overriding discord.py help command """
    # pylint says this is not needed:
    # def __init__(self):
    #    super().__init__()

    async def send_bot_help(self, mapping):
        for cog in mapping:
            await self.get_destination().send(f"{cog.qualified_name[:-3]}: {[command.name for command in mapping[cog]]}")

    async def send_cog_help(self, cog):
        await self.get_destination().send(f"{cog.qualified_name[:-3]}: {[command.name for command in cog.get_commands()]}")

    async def send_group_help(self, group):
        await self.get_destination().send(f"{group.name}: {[command.name for index, command in enumerate(group.commands)]}")

    async def send_command_help(self, command):
        await self.get_destination().send(command.name)

class DiscordBot(commands.Bot):
    """ Class for handling Dicord Bot startup and execution """
    def __init__(self):
        intents = Intents.default()
        intents.message_content = True
        help_command = commands.DefaultHelpCommand(show_parameter_descriptions=False, no_category = 'Help Cmds') # Remove the "No Category" in !help
        super().__init__(command_prefix='!', intents=intents, help_command=help_command) # help_command=MyHelpCommand())
        self.db_controller = DBController()

    async def on_ready(self) -> None:
        """ Bot startup """
        print(f'{self.user} has started.')
        await self.load_cogs()

    async def load_cogs(self):
        """ 
        Load cogs into the bot. 
        Current working directory must be within the main Discord Reminder Bot Folder. 
        """
        for filename in os.listdir("./cogs"):
            if filename.endswith(".py") and filename != "__init__.py":
                await self.load_extension(f'cogs.{filename[:-3]}')
                print(f"Loaded Cog: {filename[:-3]}")

def main() -> None:
    """ main method """
    load_dotenv()
    token: Final[str] = os.getenv('DISCORD_TOKEN')
    bot = DiscordBot()
    bot.run(token)

if __name__ == '__main__':
    main()
