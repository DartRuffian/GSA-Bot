""" Utilities class for useful functions """

# Imports
import discord
from discord.ext import commands
from traceback import format_exception
import os


class Utils:
    async def log_error(bot, ctx, error):
        error_channel = bot.get_guild(844325997566099497).get_channel(892221441481777202)
        message, error_embed = Utils.create_error_embed(bot, ctx.message.content, error)
        
        await error_channel.send(message or "", embed=error_embed)

        if isinstance(error, commands.errors.CommandNotFound):
            await ctx.message.reply(f"The command `{ctx.message.content.split(' ')[0]}` was not recognized. Here is a list of all commands.")
            await ctx.send_help()

        else:
            await ctx.message.reply(embed=error_embed)

    def create_error_embed(bot, command, error):
        hide_args_aliases = [
            # list of commands/aliases to hide the arguments of, most notably the anonymous confession command
            "anonymous_confession",
            "anon_confess",
            "confess",
            "ac",
        ]

        for alias in hide_args_aliases:
            if command[1:].startswith(alias):
                command = command.split(" ")[0] + " <arguments have been hidden for privacy reasons>"

        error_embed = discord.Embed (
            title="An Error has Occurred",
            description=f"Message:\n```\n{command}\n```\nError:\n```py\n{''.join(format_exception(type(error), error, None))}\n```",
            color=bot.transparent_color
        )
        error_embed.set_author (
            name=bot.user.name,
            icon_url=bot.user.avatar_url
        )

        non_critical_errors = [
            discord.ext.commands.errors.CommandNotFound,
            discord.ext.commands.errors.CommandOnCooldown,
            discord.ext.commands.errors.MissingRequiredArgument,
            discord.ext.commands.errors.MissingPermissions,
            discord.ext.commands.errors.PrivateMessageOnly
        ]

        message = None
        if type(error) not in non_critical_errors:
            message = f"The following error has been flagged as `critical`.\n||<@{bot.owner_id}>||"
        
        return (message, error_embed)

    def log(bot, message: str) -> None:
        os.chdir(f"{bot.BASE_DIR}/resources")
        with open("bot.log", "a") as f:
            f.write(message + "\n\n")
        os.chdir(bot.BASE_DIR)