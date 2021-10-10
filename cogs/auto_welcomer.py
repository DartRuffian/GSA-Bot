# Discord Imports
import discord
from discord.ext import commands

class Welcomer(commands.Cog):
    """ Welcomer """
    def __init__(self, bot):
        self.bot = bot


    @commands.Cog.listener()
    async def on_member_join(self, member):
        await member.send("Welcome to the official GSA discord server for Spring Hill! \nTo \"officially\" join the server, write up an intro for yourself in <#844658740451606559> and read the <#844663424679804929> channel! \nAfter doing both of those, hit the green checkmark in the rules channel to be given access to the rest of the server!")


def setup(bot):
    bot.add_cog(Welcomer(bot))