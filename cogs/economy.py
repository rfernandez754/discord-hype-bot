""" Module contains a Cog for handling the economy. """
from discord.ext import commands

class EconomyCog(commands.Cog):
    """ This cog handles general economy commands. """

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def register(self, ctx):
        """ Attempts to register a user to the economy game meaning theyre added to the database """
        user_id = str(ctx.author.id)
        # Check if user is already registered
        if self.bot.dbcontroller.check_user_exists(user_id):
            await ctx.send("You are already registered!")
        else:
            # Insert new user into the database
            self.bot.dbcontroller.add_user(user_id)
            await ctx.send("You are now registered!")

    @commands.command(name='balance', help='Check your current balance')
    async def balance(self, ctx):
        """ Check the user's current balance """
        user_id = str(ctx.author.id)
        balance = self.bot.dbcontroller.get_user_balance(user_id)
        if balance is not None:
            await ctx.send(f"Your balance is {balance} gold.")
        else:
            await ctx.send("You don't have a balance.")

    @commands.command(name='gold', help='Adds gold to your account')
    async def gold(self, ctx):
        """ Check the user's current balance """
        user_id = str(ctx.author.id)
        self.bot.dbcontroller.add_gold(user_id, 50)

async def setup(bot):
    """ Setups this Cog with the Discord Bot """
    print("Inside of setup function......")
    await bot.add_cog(EconomyCog(bot))
