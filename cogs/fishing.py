""" Module contains a Cog for handling the economy. """
import logging
from discord.ext import commands
from fishing_util import FishingUtil

class FishingCog(commands.Cog):
    """ This cog handles fishing commands. """

    def __init__(self, bot):
        self.bot = bot
        self.fishing = FishingUtil()

    @commands.command(name='fish', help='Attempt to catch and sell a fish')
    @commands.cooldown(1,1,commands.BucketType.user)
    async def fish(self, ctx):
        """ Attempt to catch a fish to sell for gold! """
        user_id = str(ctx.author.id)
        result_message, result_earnings = self.fishing.catch_fish()
        logging.info("Fish caught by %s", user_id)
        economy_cog = self.bot.get_cog('EconomyCog')
        if economy_cog.check_if_registered(ctx, user_id):
            self.bot.db_controller.add_gold(user_id, result_earnings)
            await ctx.send(result_message)

async def setup(bot):
    """ Setups this Cog with the Discord Bot """
    await bot.add_cog(FishingCog(bot))
