""" Utilities class for useful functions """

# Imports
from discord.ext import commands
from json import load
from os import chdir


class Utils:
    def is_owner():
        # Return whether a given user is the bot author
        async def predicate(ctx):
            return ctx.author.id == 400337254989430784
        return commands.check(predicate)