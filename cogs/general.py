""" Module contains a Cog for handling General user commands and monitoring. """
from discord.ext import commands

class General(commands.Cog):
    """ This cog handles general user commands and error watching. """

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        """ Outputs a message to the user when they run a command on cooldown """
        if isinstance(error, commands.CommandOnCooldown):
            cooldown = error.retry_after
            if cooldown >= 60:
                await ctx.send("This command is on cooldown, "
                              f"you can use it in {round(cooldown/60)}m")
            else:
                await ctx.send("This command is on cooldown, "
                              f"you can use it in {round(cooldown,2)}s")
        else:
            print(error)

    @commands.command()
    async def hello(self, ctx, *, arg):
        """ Test command to get bot response. Make sure to give args """
        await ctx.send(f"Hey there, I got your command: {arg}")

    @commands.Cog.listener()
    async def on_member_join(self, member):
        """ For when a new member joins """
        # this may need the proper intents
        await member.send('Welcome to the server!')

async def setup(bot):
    """ Setups this Cog with the Discord Bot """
    await bot.add_cog(General(bot))
