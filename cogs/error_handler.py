""" Error Handler """

# Discord Imports
import discord
from discord.ext import commands

# Other Imports
from traceback import format_exception

class Error_Handler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        # Handle errors that may be raised
        error_channel = self.bot.get_guild(844325997566099497).get_channel(892221441481777202)
        error_embed = discord.Embed (
            title="An Error has Occurred",
            description=f"```py\n{''.join(format_exception(type(error), error, None))}\n```"
        )
        error_embed.set_author (
            name=self.bot.user.name,
            icon_url=self.bot.user.avatar_url
        )

        non_critical_errors = [
            discord.ext.commands.errors.CommandNotFound,
            discord.ext.commands.errors.CommandOnCooldown,
            discord.ext.commands.errors.MissingRequiredArgument,
            discord.ext.commands.errors.MissingPermissions
        ]

        message = None
        if type(error) not in non_critical_errors:
            message = "The following error has been flagged as `critical`.\n||<@400337254989430784>||"
        
        await error_channel.send(message or "", embed=error_embed)


def setup(bot):
    bot.add_cog(Error_Handler(bot))