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
            days, hours_remainder = divmod(cooldown, 86400)  # 86400 seconds in a day
            hours, minutes_remainder = divmod(hours_remainder, 3600)  # 3600 seconds in an hour
            minutes, seconds = divmod(minutes_remainder, 60)

            cooldown_message_parts = []

            if days >= 1:
                cooldown_message_parts.append(f"{days}d")
            if hours >= 1:
                cooldown_message_parts.append(f"{hours}h")
            if minutes >= 1:
                cooldown_message_parts.append(f"{minutes}m")

            seconds = round(seconds, 2)
            cooldown_message_parts.append(f"{seconds}s")

            cooldown_message = " ".join(cooldown_message_parts)
            await ctx.send(f"This command is on cooldown, you can use it in {cooldown_message}")
        else:
            print(error)

    @commands.command()
    async def hello(self, ctx, *, arg):
        """ Test command to get bot response. Make sure to give args """
        await ctx.send(f"Hey there, I got your command with args: {arg}")

    @commands.Cog.listener()
    async def on_member_join(self, member):
        """ For when a new member joins """
        # this may need the proper intents
        await member.send('Welcome to the server!')

async def setup(bot):
    """ Setups this Cog with the Discord Bot """
    await bot.add_cog(General(bot))
