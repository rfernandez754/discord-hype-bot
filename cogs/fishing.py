""" Module contains a Cog for handling the economy. """
import logging
from discord.ext import commands
from fishing_util import FishingUtil

# Used for ordering in Fishing Leaderboards
RARITY_MAP = { "Common" : 0, "Uncommon" : 1, "Rare" : 2, "Very Rare" : 3,
               "Legendary" : 4, "Mythic" : 5, "Godly" : 6}

class Fishing(commands.Cog):
    """ This cog handles fishing commands. """

    def __init__(self, bot):
        self.bot = bot
        self.fishing = FishingUtil()

    @commands.command(name='fish', help='Attempt to catch and sell a fish')
    @commands.cooldown(1,1,commands.BucketType.user)
    async def fish(self, ctx):
        """ Attempt to catch a fish to sell for gold! """
        user_id = str(ctx.author.id)
        message, earnings, species, size, rarity = self.fishing.catch_fish()
        logging.info("Fish caught by %s", user_id)
        self.bot.db_controller.add_gold(user_id, earnings)
        if rarity != "Joke" and \
        self.bot.db_controller.check_if_new_biggest_fish(species, RARITY_MAP[rarity], size, user_id):
            message += "```You have caught the biggest fish of this species! Type !biggest```"
        await ctx.send(message)

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
    await bot.add_cog(Fishing(bot))
