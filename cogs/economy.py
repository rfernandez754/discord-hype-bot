""" Module contains a Cog for handling the economy. """
from discord.ext import commands

class EconomyCog(commands.Cog):
    """ This cog handles general economy commands. """

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
    async def register(self, ctx):
        """ Attempts to register a user to the economy game 
        meaning the user is added to the database """
        user_id = str(ctx.author.id)
        # Check if user is already registered
        if self.bot.db_controller.check_user_exists(user_id):
            await ctx.send("You are already registered!")
        else:
            # Insert new user into the database
            self.bot.db_controller.add_user(user_id)
            await ctx.send("You are now registered!")

    @commands.command(name='balance', help='Check your current balance')
    async def balance(self, ctx):
        """ Check the user's current balance """
        user_id = str(ctx.author.id)
        balance = self.bot.db_controller.get_user_balance(user_id)
        if balance is not None:
            await ctx.send(f"Your balance is {balance} gold.")
        else:
            await ctx.send("You are not registered. "
                          f"Use {self.bot.command_prefix}register to register.")

    @commands.command(name='gold', help='Adds gold to your account')
    @commands.cooldown(1,10,commands.BucketType.user)
    async def gold(self, ctx):
        """ Adds gold to the user's balance """
        amount = 50
        user_id = str(ctx.author.id)
        if self.check_if_registered(ctx, user_id):
            self.bot.db_controller.add_gold(user_id, amount)
            await ctx.send(f"You gained {amount} gold!")

    @commands.command(name='mystery', help='Does something mysterious')
    @commands.cooldown(1,60,commands.BucketType.user)
    async def mystery(self, ctx):
        """ Does something mysterious from a list of possibilities """
        pass

    def check_if_registered(self, ctx, user_id):
        """ Will tell the user to register if not registered """
        if not self.bot.db_controller.check_user_exists(user_id):
            ctx.send("You are not registered. "
                          f"Use {self.bot.command_prefix}register to register.")
            return False
        return True


async def setup(bot):
    """ Setups this Cog with the Discord Bot """
    await bot.add_cog(EconomyCog(bot))
