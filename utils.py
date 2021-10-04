""" Utilities class for useful functions """

# Imports
import discord
from traceback import format_exception


class Utils:
    def create_error_embed(bot, command, error):
        error_embed = discord.Embed (
            title="An Error has Occurred",
            description=f"Message:\n```\n{command}\n```\nError:\n```py\n{''.join(format_exception(type(error), error, None))}\n```",
            color=0x2F3136
        )
        error_embed.set_author (
            name=bot.user.name,
            icon_url=bot.user.avatar_url
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
        
        return (message, error_embed)