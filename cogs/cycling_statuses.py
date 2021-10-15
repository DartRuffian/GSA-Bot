# Discord Imports
import discord
from discord.ext import commands, tasks

# Other Imports
from random import choice as rand_choice

class Cycling_Statuses(commands.Cog):
    """ Pick a random status from a list """
    def __init__(self, bot):
        self.bot = bot
        self.statuses = []
        with open(f"{self.bot.BASE_DIR}/resources/statuses.txt", "r") as f:
            self.statuses.extend([line.strip(" \n") for line in f.readlines()])
    
    @tasks.loop(seconds=15)
    async def update_status(self):
        await self.bot.change_presence(activity=discord.Game(rand_choice(self.statuses)))
    
    @commands.Cog.listener()
    async def on_ready(self):
        self.update_status.start()


def setup(bot):
    bot.add_cog(Cycling_Statuses(bot))