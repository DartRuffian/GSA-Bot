""" Main Bot File """
# Discord Imports
import discord
from discord.ext import commands

# Keep Bot Online
from webserver import keep_alive

# Other Imports
from datetime import datetime            # Get bot launch time
from os import listdir, getcwd, environ  # Load cogs/environment vars (token)
from utils import Utils                  # Utility functions
from random import randint               # Random Color


def get_token() -> str:
    # Load token
    try:
        # If running locally
        with open("tokens.txt", "r") as f:
            token = f.read().split("\n")[0]
    except FileNotFoundError:
        # If running on server
        token = environ.get("DISCORD_BOT_SECRET")

    return token


def main() -> None:
    # Define the bot
    intents = discord.Intents.default()
    intents.members = True
    intents.presences = True
    intents.emojis = True
    bot = commands.Bot(
        command_prefix=commands.when_mentioned_or("$"),
        owner_id=400337254989430784,
        case_insensitive=True,
        intents=intents,
    )

    # Custom Attributes
    bot.BASE_DIR = getcwd()
    bot.LAUNCH_TIME = datetime.utcnow()
    bot.utils = Utils(bot)
    bot.get_random_color = lambda: int("%06x" % randint(0, 0xFFFFFF), 16)
    bot.TRANSPARENT_COLOR = 0x2F3136

    # Load all cogs
    for filename in listdir("./cogs"):
        if filename.endswith(".py"):
            bot.load_extension(f"cogs.{filename[:-3]}")

    @bot.event
    async def on_ready():
        # Called whenever the bot connects to Discord
        print("Logged in")
        print(f"Username: {bot.user.name}")
        print(f"User Id : {bot.user.id}")

        bot.guild = bot.get_guild(937426313998917692)
        bot.log_channel = bot.guild.get_channel(937924972695941171)

    keep_alive()
    TOKEN = get_token()
    bot.run(TOKEN)


if __name__ == "__main__":
    main()
