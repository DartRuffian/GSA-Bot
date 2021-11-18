# Discord Imports
import discord
from discord.ext import commands

# Other Imports
import requests
from os import environ

# Utils
from utils import Utils


class ArtUtils(commands.Cog, name="Artist Utilities"):
    """Helpful commands for any potential artists"""
    def __init__(self, bot):
        self.bot = bot
        try:
            with open("tokens.txt", "r") as f:
                self.RBG_TOKEN = f.read().split("\n")[1]
        except FileNotFoundError:
            self.RBG_TOKEN = environ.get("RBG_TOKEN") 

    @commands.command(
        brief="Takes an image and returns that image with their backgrounds removed.",
        description="Runs the given image through <https://www.remove.bg>'s API.",
        aliases=["rbg", "rmvbg"]
    )
    async def remove_background(self, ctx, image_link=None):
        if not image_link and not ctx.message.attachments:
            await ctx.message.reply("Make sure to either send an image link or upload an image in your message!",
                                    mention_author=False)
            return

        await ctx.send("Processing your image, this may take a while..."
                       "You'll be pinged when your image is done, or if an error occurred.")
        async with ctx.channel.typing():
            response = requests.post(
                "https://api.remove.bg/v1.0/removebg",
                data={
                    "image_url": image_link or ctx.message.attachments[0].url,
                    "size": "auto"
                },
                headers={"X-Api-Key": self.RBG_TOKEN},
            )
            if response.status_code == requests.codes.ok:
                with open("output.png", "wb") as out:
                    out.write(response.content)
                await ctx.message.reply(file=discord.File("output.png"))
            else:
                await ctx.message.reply(f"An error occurred while processing your image:"
                                        f"\nError Code: {response.status_code} - {response.text}")


def setup(bot):
    bot.add_cog(Art_Utils(bot))
