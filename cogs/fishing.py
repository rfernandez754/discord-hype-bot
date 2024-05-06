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
        economy_cog = self.bot.get_cog('EconomyCog')
        if economy_cog.check_if_registered(ctx, user_id):
            result_message, result_earnings, result_species, result_size, result_rarity = self.fishing.catch_fish()
            logging.info("Fish caught by %s", user_id)
            self.bot.db_controller.add_gold(user_id, result_earnings)
            if result_rarity != "Joke" and self.bot.db_controller.check_if_new_biggest_fish(result_species, result_size, user_id):
                result_message += " You have caught the biggest fish of this species! Type !biggest"
            await ctx.send(result_message)

    @commands.command(name='biggest', help='Shows the leaderboard of biggest fish caught')
    async def biggest(self, ctx):
        """ Attempt to catch a fish to sell for gold! """
        result_message = self.bot.db_controller.get_fish_leaderboard()
        if result_message:
            formatted_rows = []
            formatted_rows.append("Fishing Size Leaderboard")
            formatted_rows.append("")
            formatted_rows.append("Fish Name            Fish Size      Username")
            for row in result_message:
                fish_name = row[0]
                size = f"{float(row[1]):.2f} cm"
                user_id = row[2]
                # Need to grab discord username from user_id
                user = await self.bot.fetch_user(user_id)
                username = user.name
                formatted_row = f"{fish_name:<20} {size:<10}     {username}"
                formatted_rows.append(formatted_row)

            leaderboard_message = "\n".join(formatted_rows)
            # Sending as code block for better formatting
            await ctx.send(f"```{leaderboard_message}```")
        else:
            await ctx.send("There are currently no fish on the leaderboards")

async def setup(bot):
    """ Setups this Cog with the Discord Bot """
    await bot.add_cog(FishingCog(bot))
