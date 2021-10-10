# Discord Imports
import discord
from discord.ext import commands

# Other Imports
from utils import Utils

class Error_Handler(commands.Cog):
    """ Global Error Handler """
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        # Handle errors that may be raised
        if hasattr(ctx.command, "on_error"):
            # If the command already has a specific error handler, don't run anything here
            return

        await Utils.log_error(self.bot, ctx, error)


def setup(bot):
    bot.add_cog(Error_Handler(bot))