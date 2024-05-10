""" Module contains a Cog for handling the economy. """
from discord.ext import commands
import random

class Economy(commands.Cog):
    """ This cog handles general economy commands. """

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='balance', help='Check your current balance')
    async def balance(self, ctx):
        """ Check the user's current balance """
        user_id = str(ctx.author.id)
        balance = self.bot.db_controller.get_user_balance(user_id)
        formatted_balance = f"{balance:,}" # Add commas
        await ctx.send(f"Your balance is {formatted_balance} gold.")

    @commands.command(name='daily', help='Daily command to get gold')
    @commands.cooldown(1,86400,commands.BucketType.user)
    async def daily(self, ctx):
        """ Adds gold to the user's balance """
        amount = 50
        user_id = str(ctx.author.id)
        self.bot.db_controller.add_gold(user_id, amount)
        await ctx.send(f"You gained {amount} gold!")

    @commands.command(name='mystery', help='Does something mysterious')
    @commands.cooldown(1,86400,commands.BucketType.user)
    async def mystery(self, ctx):
        """ Does something mysterious from a list of possibilities """
        choice = random.randint(1,100)
        if choice <= 10:
            random_amount = random.randint(1,100)
            self.bot.db_controller.add_gold(str(ctx.author.id), random_amount)
            await ctx.send(f"You find a {random_amount} gold in a trash can on the side of the road. You rat...")
        elif choice <= 20:
            random_amount = random.randint(1,75)
            self.bot.db_controller.subtract_gold(str(ctx.author.id), random_amount)
            await ctx.send(f"You invest some cash into a memecoin. Aaaaand its gone. Say goodbye to {random_amount} gold.")
        elif choice <= 30:
            await ctx.send("You play league of legends? Wow... I have nothing to say... or do...")
        elif choice <= 40:
            random_amount = random.randint(1,10)
            self.bot.db_controller.add_gold(str(ctx.author.id), random_amount)
            await ctx.send(f"You say Shmee Shmee and {random_amount} gold appears in your pocket.")
        elif choice <= 50:
            random_amount = random.randint(1,10)
            self.bot.db_controller.add_gold(str(ctx.author.id), random_amount)
            await ctx.send(f"You say Shmee Shmee and {random_amount} gold appears in your pocket.")
        elif choice <= 60:
            self.bot.db_controller.add_gold(str(ctx.author.id), 200)
            await ctx.send("You pass GO. Here's 200 gold.")
        elif choice <= 70:
            if self.bot.db_controller.count_users() >= 2:
                random_user = self.bot.db_controller.get_random_user()
                random_amount = random.randint(1,200)
                stolen_amount = self.bot.db_controller.steal_gold(str(ctx.author.id), random_user, random_amount)
                stealer = await self.bot.fetch_user(str(ctx.author.id))
                stealer_name = stealer.name
                victim = await self.bot.fetch_user(random_user)
                victim_name = victim.name
                if stolen_amount:
                    await ctx.send(f"Oh no! {stealer_name} just stole {stolen_amount} from {victim_name}! No ones doing anything to help? Classic bystander effect...")
                else:
                    await ctx.send(f"{stealer_name} attempts to steal from {victim_name} but turns out they are completely broke.")
            else:
                await ctx.send("You are going to steal gold but theres nobody you find to steal from.")
        elif choice <= 80:
            if self.bot.db_controller.count_users() >= 2:
                random_user = self.bot.db_controller.get_random_user()
                random_amount = random.randint(1,200)
                given_amount = self.bot.db_controller.steal_gold(random_user, str(ctx.author.id), random_amount)
                gifter = await self.bot.fetch_user(str(ctx.author.id))
                gifter_name = gifter.name
                giftee = await self.bot.fetch_user(random_user)
                giftee_name = giftee.name
                if given_amount:
                    await ctx.send(f"Oh no! {gifter_name} just stole {given_amount} from {giftee_name}! No ones doing anything to help? Classic bystander effect...")
                else:
                    await ctx.send(f"{gifter_name} was going to gift money to {giftee_name} but turns out they are completely broke.")
            else:
                await ctx.send("You are going to gift gold but theres nobody you find to gift to.")
        elif choice <= 90:
            for user in self.bot.db_controller.get_users():
                self.bot.db_controller.add_gold(user, 10)
            await ctx.send("Oprah appears from above in a helicopter and gives everyone 10 gold.")
        else:
            await ctx.send("Nothing Happens!")

    @commands.command(name='lb', help='Shows the gold leaderboard')
    async def lb(self, ctx):
        """ Fetches the gold data of every user to display on a leaderboard """
        result_message = self.bot.db_controller.get_gold_leaderboard()
        if result_message:
            formatted_rows = []
            formatted_rows.append("Gold Leaderboard")
            formatted_rows.append("")
            formatted_rows.append("Username          Balance")
            for row in result_message:
                user_id = row[0]
                balance = row[1]
                # Need to grab discord username from user_id.
                # This step takes too long. TODO find another solution.
                user = await self.bot.fetch_user(user_id)
                username = user.name
                formatted_row = f"{username}          {balance:,}"
                formatted_rows.append(formatted_row)

            leaderboard_message = "\n".join(formatted_rows)
            # Sending as code block because it looks better
            await ctx.send(f"```{leaderboard_message}```")
        else:
            await ctx.send("There are currently no fish on the leaderboards")

async def setup(bot):
    """ Setups this Cog with the Discord Bot """
    await bot.add_cog(Economy(bot))
