""" Module contains a Cog for handling the economy. """
import logging
import math
import asyncio
from discord.ext import commands
from fishing_util import FishingUtil

# Used for ordering in Fishing Leaderboards
RARITY_MAP = { "Common" : 0, "Uncommon" : 1, "Rare" : 2, "Very Rare" : 3,
               "Legendary" : 4, "Mythic" : 5, "Godly" : 6 }

ROD_TYPE_MAP = {
    1: "Shoddy Wooden Rod",
    2: "Oak Wood Rod",
    3: "Basic Iron Rod",
    4: "Reinforced Steel Rod",
    5: "Adamantine Rod",
    6: "Advanced Carbon Fiber Rod",
    7: "Legendary Admiral Rod",
    8: "Magical Crystal Rod",
    9: "Ancient Dragon Rod",
    10: "Titanium Alloy Rod",
    11: "Celestial Gold Rod",
    12: "Ethereal Diamond Rod",
    13: "Void Essence Rod",
    14: "Dimensional Rift Rod",
    15: "Cosmic Nexus Rod",
    16: "Timeless Chrono Rod",
    17: "Infinite Omegon Rod",
    18: "4 Dimensional God Rod",
    19: "5 Dimensional Infinity Rod",
    20: "Infinite Dimensional Rod",
    21: "Multiversal Rod",
}


class Fishing(commands.Cog):
    """ These are the commands for the fishing minigame. Catch and sell fish. Compete for the size leaderboards. Level up! """

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
        current_rod_lvl = self.bot.db_controller.get_level(user_id, "rod")
        fishing = FishingUtil(current_fishing_lvl, current_rod_lvl)
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

    @commands.command(name='level', help='Displays your current fishing level and xp')
    async def level(self, ctx):
        """ Displays your current fishing level and xp. """
        if ctx.author.nick:
            name = ctx.author.nick
        else:
            name = ctx.author.display_name
        user_id = str(ctx.author.id)
        level = self.bot.db_controller.get_level(user_id, "fishing")
        current_xp = self.bot.db_controller.get_xp(user_id, "fishing")
        xp_to_level = math.ceil(100 * (1.1 ** (level - 1))) - current_xp
        await ctx.send(f"Hi {name}, you are fishing level {level}. You have {current_xp} xp and need {xp_to_level} more xp to level up.")

    @commands.command(name='rod', help='Displays your current rod level and name')
    async def rod(self, ctx):
        """ Displays your current rod level and name. """
        if ctx.author.nick:
            name = ctx.author.nick
        else:
            name = ctx.author.display_name
        user_id = str(ctx.author.id)
        rod_level = self.bot.db_controller.get_level(user_id, "rod")
        await ctx.send(f"```Hi {name}, you have a {ROD_TYPE_MAP[rod_level]}. This rod's level is {rod_level}.```")

    @commands.command(name='upgrade', help='Attemps to upgrade your fishing rod')
    async def upgrade(self, ctx):
        """ Attemps to upgrade your fishing rod. """
        def check(message): # Make sure it is the same user replying in the same channel to bot question
            return message.author == ctx.author and message.channel == ctx.channel

        if ctx.author.nick:
            name = ctx.author.nick
        else:
            name = ctx.author.display_name
        user_id = str(ctx.author.id)
        rod_level = self.bot.db_controller.get_level(user_id, "rod")
        if rod_level + 1 not in ROD_TYPE_MAP:
            await ctx.send("```You have already reached the max level fishing rod!```")
            return
        gold_required = (2 ** (rod_level-1)) * 100
        balance = self.bot.db_controller.get_user_balance(user_id)
        formatted_balance = f"{balance:,}" # Add commas
        formatted_gold_required = f"{gold_required:,}" # Add commas

        if balance < gold_required:
            await ctx.send(f"```Hi {name}, you have {formatted_balance} gold but need {formatted_gold_required} to upgrade your rod to a {ROD_TYPE_MAP[rod_level+1]}.```")
        else:
            await ctx.send(f"```Hi {name}, you have {formatted_balance} gold. Would you like to upgrade your rod to a {ROD_TYPE_MAP[rod_level+1]} for {formatted_gold_required} gold?```")

            try:
                message = await self.bot.wait_for('message', timeout=30.0, check=check)  # Wait for user response
                if "yes" in message.content.lower() or message.content.lower() == "y":
                    rod_level += 1
                    self.bot.db_controller.update_level(user_id, "rod", rod_level)
                    self.bot.db_controller.subtract_gold(user_id, gold_required)
                    await ctx.send(f"```Congrats! You have upgraded your fishing rod to a {ROD_TYPE_MAP[rod_level]}.```")
                else:
                    await ctx.send(f"```You don't want it... thats fine !```")
            except asyncio.TimeoutError:
                await ctx.send("```You took too long to respond.```")

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
