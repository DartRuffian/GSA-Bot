# Discord Imports
import discord
from discord.ext import commands

# Keep Bot Online
from webserver import keep_alive

# Other imports
from random import randint
from os import listdir, getcwd, environ

# Define the bot
intents = discord.Intents.default()
intents.members = True
bot = commands.Bot (
    command_prefix=commands.when_mentioned_or("$"),
    intents=intents,
    case_insensitive=True,
)

# Other attributes
bot.AUTHOR = 400337254989430784
bot.BASE_DIR = getcwd()
bot.get_random_color = lambda: int("%06x" % randint(0, 0xFFFFFF), 16)


@bot.event 
async def on_ready():
    # Called when the bot connects to Discord
    print("Logged in")
    print(f"Username: {bot.user.name}")
    print(f"Userid  : {bot.user.id}")

# Load all cogs in the "cogs" subfolder
for filename in listdir("./cogs"):
    if filename.endswith(".py"):
        bot.load_extension(f"cogs.{filename[:-3]}")


keep_alive()
try:
    with open("token.txt","r") as f:
        TOKEN = f.read()
except FileNotFoundError:
    TOKEN = environ.get("DISCORD_BOT_SECRET") 

bot.run(TOKEN)