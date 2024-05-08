""" Module contains a Cog for handling the economy. """
from discord.ext import commands

class Economy(commands.Cog):
    """ This cog handles general economy commands. """

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def register(self, ctx): # TODO delete this once we know we dont need this
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
        formatted_balance = f"{balance:,}" # Add commas
        await ctx.send(f"Your balance is {formatted_balance} gold.")

    @commands.command(name='gold', help='Adds gold to your account')
    @commands.cooldown(1,10,commands.BucketType.user)
    async def gold(self, ctx):
        """ Adds gold to the user's balance """
        amount = 50
        user_id = str(ctx.author.id)
        self.bot.db_controller.add_gold(user_id, amount)
        await ctx.send(f"You gained {amount} gold!")

    @commands.command(name='mystery', help='Does something mysterious')
    @commands.cooldown(1,60,commands.BucketType.user)
    async def mystery(self, ctx):
        """ Does something mysterious from a list of possibilities """
        pass

    def check_if_registered(self, ctx, user_id): # TODO delete this once we know we dont need this
        """ Will tell the user to register if not registered """
        if not self.bot.db_controller.check_user_exists(user_id):
            ctx.send("You are not registered. "
                          f"Use {self.bot.command_prefix}register to register.")
            return False
        return True


async def setup(bot):
    """ Setups this Cog with the Discord Bot """
    await bot.add_cog(Economy(bot))
