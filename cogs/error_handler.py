""" Error Handler """

# Discord Imports
import discord
from discord.ext import commands

# Other Imports
from utils import Utils

class Error_Handler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        # Handle errors that may be raised
        if hasattr(ctx.command, 'on_error'):
            # If the command already has a specific error handler, don't run anything here
            return

        error_channel = self.bot.get_guild(844325997566099497).get_channel(892221441481777202)
        message, error_embed = Utils.create_error_embed(self.bot, ctx.message.content, error)
        
        await error_channel.send(message or "", embed=error_embed)

        if isinstance(error, commands.errors.CommandNotFound):
            await ctx.send(f"The command `{ctx.message.content.split(' ')[0]}` was not recognized. Here is a list of all commands.")
            await ctx.send_help()

        else:
            await ctx.send(embed=error_embed)


def setup(bot):
    bot.add_cog(Error_Handler(bot))