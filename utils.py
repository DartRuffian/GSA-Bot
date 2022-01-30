# Imports
import discord
from discord.ext import commands
from traceback import format_exception
import os
from enum import Enum, auto


class StatusType(Enum):
    ERROR = auto()
    WARNING = auto()
    OK = auto()


class Utils:
    """Utilities class for useful functions"""
    def __init__(self, bot: discord.ext.commands.Bot):
        self._bot = bot

    async def log_error(self, ctx, error) -> None:
        error_channel = self._bot.get_guild(937426313998917692).get_channel(937444414324887572)
        message, error_embed = self.create_error_embed(ctx.message.content, error)

        await error_channel.send(message or "", embed=error_embed)
        self.log(message)

        if isinstance(error, commands.errors.CommandNotFound):
            await ctx.message.reply(
                f"""The command `{ctx.message.content.split(' ')[0]}` was not recognized.
Here is a list of all commands."""
            )
            await ctx.send_help()

        else:
            await ctx.message.reply(embed=error_embed)

    def create_error_embed(self, command, error) -> tuple[str, discord.Embed]:
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

        error_embed = discord.Embed(
            title="An Error has Occurred",
            description=f"""Message:
```
{command}
```
Error:
```py
{"".join(format_exception(type(error), error, None))}
```""",
            color=self._bot.TRANSPARENT_COLOR
        )
        error_embed.set_author(
            name=self._bot.user.name,
            icon_url=self._bot.user.avatar_url
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
            message = f"The following error has been flagged as `critical`.\n||<@{self._bot.owner_id}>||"

        return message, error_embed

    def log(self, message: str) -> None:
        os.chdir(f"{self._bot.BASE_DIR}/resources")
        with open("bot.log", "a") as f:
            f.write(message + "\n\n")
        os.chdir(self._bot.BASE_DIR)

    @staticmethod
    def get_clean_list(lst: list) -> str:
        if len(lst) == 1:
            return lst[0]
        if len(lst) == 2:
            return f"{lst[0]} or {lst[1]}"

        return (", ".join([i for i in lst[0:-1]])) + f", or {lst[-1]}"
