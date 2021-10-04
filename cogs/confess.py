""" Anonymous Confessions """

# Discord Imports
import discord
from discord.ext import commands

# Other Imports
from utils import Utils

class Confessions(commands.Cog, name="Confessions"):
    def __init__(self, bot):
        self.bot = bot


    @commands.command (
        aliases=["ac", "confess", "anon_confess"],
        brief="Makes an anonymous confession",
        description="This command only works in a direct message with the bot, which takes a confession and sends it for you to keep it anonymous. Nothing is recorded."
    )
    @commands.dm_only()
    async def anonymous_confession(self, ctx, *, message):
        guild = self.bot.get_guild(844325997566099497)
        confession_channel = guild.get_channel(847293323672682506)

        if "<" in message or ">" in message:
            await ctx.author.send("Note that the angle brackets, the '<' and '>' characters, only mean that the message can be multiple words and aren't required.\n\nFor example, this is a perfectly good example of running the command: \n`$confess You're a cutie`")

        confession_embed = discord.Embed (
            description=message,
            color=self.bot.get_random_color()
        )

        await confession_channel.send(embed=confession_embed)
        await ctx.author.send("Your confession has been recorded.")
    
    @anonymous_confession.error
    async def confession_error(self, ctx, error):
        if isinstance(error, commands.errors.PrivateMessageOnly):
            await ctx.message.delete()
            await ctx.send("This command can only be used in a private message with the bot, and your message has been deleted so that it won't be seen by other users.", delete_after=3)
            await ctx.author.send("Instead, run the command here.")
        
        elif isinstance(error, commands.errors.MissingRequiredArgument):
            await ctx.send("Looks like you missed an argument there, make sure you type `$confess` (or any other alias for the command) followed by your message.")


        error_channel = self.bot.get_guild(844325997566099497).get_channel(892221441481777202)
        message, error_embed = Utils.create_error_embed(self.bot, ctx.message.content, error)

        await error_channel.send(message or "", embed=error_embed)
        await ctx.send(embed=error_embed)      


def setup(bot):
    bot.add_cog(Confessions(bot))