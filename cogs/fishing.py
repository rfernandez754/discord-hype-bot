""" Module contains a Cog for handling the economy. """
import logging
import math
from discord.ext import commands
from fishing_util import FishingUtil

# Used for ordering in Fishing Leaderboards
RARITY_MAP = { "Common" : 0, "Uncommon" : 1, "Rare" : 2, "Very Rare" : 3,
               "Legendary" : 4, "Mythic" : 5, "Godly" : 6 }

class Fishing(commands.Cog):
    """ This cog handles fishing commands. """

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='fish', help='Attempt to catch and sell a fish')
    @commands.cooldown(3,1,commands.BucketType.user)
    async def fish(self, ctx):
        """ Attempt to catch a fish to sell for gold! """
        if ctx.author.nick:
            name = ctx.author.nick
        else:
            name = ctx.author.display_name
        user_id = str(ctx.author.id)

        skill_name = "fishing"
        current_fishing_lvl = self.bot.db_controller.get_level(user_id, skill_name)
        fishing = FishingUtil(current_fishing_lvl)
        message, earnings, species, size, rarity, earned_xp = fishing.catch_fish()
        logging.info("Fish caught by %s", user_id)
        self.bot.db_controller.add_gold(user_id, earnings)
        if rarity != "Joke" and \
        self.bot.db_controller.check_if_new_biggest_fish(species,
                                                         RARITY_MAP[rarity],
                                                         size,
                                                         user_id):
            message += "```You have caught the biggest fish of this species! Type !biggest```\n"

        current_xp = self.bot.db_controller.get_xp(user_id, skill_name)
        current_xp += earned_xp
        next_level_xp = math.ceil(100 * (1.1 ** (current_fishing_lvl - 1)))

        leveled_up = False

        while current_xp >= next_level_xp:
            logging.info("User %s has a current xp - %s thst is higher than xp needed to level up - %s. Leveling up %s!", user_id, current_xp, next_level_xp, skill_name)
            leveled_up = True
            current_fishing_lvl += 1
            self.bot.db_controller.update_level(user_id, skill_name, current_fishing_lvl)
            current_xp = current_xp - next_level_xp
            next_level_xp = math.ceil(100 * (1.1 ** (current_fishing_lvl - 1)))

        self.bot.db_controller.update_xp(user_id, skill_name, current_xp)    
        if leveled_up:
            message += f"```Congrats! Your fishing level has leveled up to level {current_fishing_lvl} !```"

        message = f"```Nice {name}, " + message # Prepend a greeting to message before sending
        await ctx.send(message)

    @commands.command(name='level', help='Displays yout current fishing level and xp')
    async def level(self, ctx):
        """ Attempt to catch a fish to sell for gold! """
        if ctx.author.nick:
            name = ctx.author.nick
        else:
            name = ctx.author.display_name
        user_id = str(ctx.author.id)
        level = self.bot.db_controller.get_level(user_id,"fishing")
        current_xp = self.bot.db_controller.get_xp(user_id,"fishing")
        xp_to_level = math.ceil(100 * (1.1 ** (level - 1))) - current_xp
        await ctx.send(f"Hi {name}, you are fishing level {level}. You have {current_xp} xp and need {xp_to_level} more xp to level up.")

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
                # Need to grab discord username from user_id.
                # This step takes too long. TODO find another solution.
                user = await self.bot.fetch_user(user_id)
                username = user.display_name
                formatted_row = f"{fish_name:<20} {size:<10}     {username}"
                formatted_rows.append(formatted_row)

            leaderboard_message = "\n".join(formatted_rows)
            # Sending as code block because it looks better
            await ctx.send(f"```{leaderboard_message}```")
        else:
            await ctx.send("There are currently no fish on the leaderboards")

async def setup(bot):
    """ Setups this Cog with the Discord Bot """
    await bot.add_cog(Fishing(bot))
