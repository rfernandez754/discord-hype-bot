""" Module contains a Cog for handling logging """
from discord.ext import commands

class Logging(commands.Cog):
    """ The cog handles general user commands. """

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        """ Stores command messages """
        # Stores only user messages that are considered commands
        if message.content[0] == self.bot.command_prefix:
            self.bot.db_controller.store_message_info(message.author.name, \
                                                    message.content, \
                                                    message.created_at)

async def setup(bot):
    """ Setups this Cog with the Discord Bot """
    await bot.add_cog(Logging(bot))
