""" Module contains a Cog for handling General user commands and monitoring. """
from discord.ext import commands

class GeneralCog(commands.Cog):
    """ This cog handles general user commands. """

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def help2(self, ctx):
        """ Prints HELP """
        await ctx.send("Help TEXT TOADD")

    @commands.command()
    async def add_role(self, ctx, *, arg):
        """ User can add an emoji to add to bots message """
        await ctx.send(f"Hey there, I got your command to add: {arg}")
        await ctx.send(f"What day of the week would you like to add the reminder for {arg}?")

    @commands.Cog.listener()
    async def on_member_join(self, member):
        """ For when a new member joins """
        # this may need the proper intents
        await member.send('Welcome to the server!')

async def setup(bot):
    """ Setups this Cog with the Discord Bot """
    await bot.add_cog(GeneralCog(bot))
