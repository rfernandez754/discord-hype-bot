""" Module contains a Cog for handling General user commands and monitoring. """
from discord.ext import commands
import discord

class GeneralCog(commands.Cog):
    """ This cog handles general user commands. """

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, content):
        """ Sends out a help message when a user enters a command incorrectly """
        print(content)
        await ctx.send("Error using that command. Please refer to !help")

    @commands.command()
    async def add(self, ctx, *, arg):
        """ Function replies to user """
        await ctx.send(f"Hey there, I got your command to add: {arg}")
        await ctx.send(f"What day of the week would you like to add the reminder for {arg}?")

        print(ctx.author.name)
        print(ctx.message.content)
        print(ctx.message.created_at)

        self.bot.db_controller.store_message_info(ctx.author.name, \
                                                  ctx.message.content, \
                                                  ctx.message.created_at)

def setup(bot):
    """ Setups this Cog with the Discord Bot """
    bot.add_cog(GeneralCog(bot))
