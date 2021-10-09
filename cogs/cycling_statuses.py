# Discord Imports
import discord
from discord.ext import commands, tasks

# Other Imports
from random import choice as rand_choice

class Cycling_Statuses(commands.Cog):
    """ Pick a random status from a list """
    def __init__(self, bot):
        self.bot = bot
        self.statuses = [
            "Trans rights are human rights!",
            "\"I hate the word homophobia. It's not a phobia. You're not scared. You're an asshole\" - Morgan Freeman",
            "Love is love!",
            "Let's get one thing straight, I'M NOT!",
            "\"Being gay is natural. Hating gay is a lifestyle choice.\" - John Fugelsang",
            "\"From a religious point of view, if God had thought homosexuality is a sin, he would not have created gay people.\" - Howard Dean"
        ]
    
    @tasks.loop(seconds=15)
    async def update_status(self):
        await self.bot.change_presence(activity=discord.Game(rand_choice(self.statuses)))
    
    @commands.Cog.listener()
    async def on_ready(self):
        self.update_status.start()


def setup(bot):
    bot.add_cog(Cycling_Statuses(bot))