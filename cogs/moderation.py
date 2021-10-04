""" Mod-Specific Commands """

# Discord Imports
import discord
from discord.ext import commands


class Moderation(commands.Cog, name="Mod Only"):
    def __init__(self, bot):
        self.bot = bot


    @commands.command (
        aliases=["delete", "del"],
        brief="Takes a number and deletes that many messages",
        description="Takes an argument `limit` and deletes that many messages from the current channel.",
        hidden=True
    )
    @commands.has_permissions(manage_messages=True)
    async def purge(self, ctx, limit: int):
        await ctx.message.delete()
        
        counter = 0
        async for message in ctx.channel.history(limit=limit):
            counter += 1
            await message.delete()
        
        await ctx.send(f"{counter} messages have been deleted.\n(This message will auto-delete in 5 seconds)", delete_after=5)


def setup(bot):
    bot.add_cog(Moderation(bot))