""" Anonymous Confessions """

# Discord Imports
import discord
from discord.ext import commands

class Confessions(commands.Cog, name="Confessions"):
    def __init__(self, bot):
        self.bot = bot


    @commands.command (
        aliases=["ac", "anon_confess"],
        brief="Makes an anonymous confession",
        description="This command only works in a direct message with the bot, which takes a confession and sends it for you to keep it anonymous. Nothing is recorded."
    )
    async def anonymous_confession(self, ctx, *, message):
        if not isinstance(ctx.channel, discord.channel.DMChannel):
            await ctx.message.delete()
            await ctx.send("This command can only be used in a private message with the bot, and your message has been deleted so that it won't be seen.", delete_after=3)
            await ctx.author.send("Instead, run the command here.")
            return
        
        guild = self.bot.get_guild(844325997566099497)
        confession_channel = guild.get_channel(847293323672682506)

        confession_embed = discord.Embed (
            title="Someone says....",
            description=message,
            color=self.bot.get_random_color()
        )

        await confession_channel.send(embed=confession_embed)
        await ctx.author.send("Your confession has been recorded.")


def setup(bot):
    bot.add_cog(Confessions(bot))