""" Quote Book """

# Discord Imports
import discord
from discord.ext import commands
from discord.utils import get

# Other Imports
from json import load, dump
from os import chdir

class Quote_Book(commands.Cog, name="Quote Book"):
    def __init__(self, bot):
        self.bot = bot


    @commands.group (
        aliases=["qb"],
        invoke_without_command=True
    )
    async def quotebook(self, ctx, *, alias):
        if ctx.invoked_subcommand is None:
            chdir(f"{self.bot.BASE_DIR}/resources")
            with open("quotes.json", "r") as f:
                quotes = load(f)
            chdir(self.bot.BASE_DIR)

            fetched_quote = None
            for quote, data in quotes.items():
                if alias in data["aliases"]:
                    fetched_quote = [quote, data]

            if fetched_quote is None:
                await ctx.send(f"No quote was found under the alias `{alias}`, please check your spelling and try again!")
                return
            
            author = get(self.bot.get_all_members(), id=fetched_quote[1]["author"])
            uploader = get(self.bot.get_all_members(), id=fetched_quote[1]["uploaded_by"])
            
            quote_embed = discord.Embed (
                title="Quote",
                description=f"> \"{fetched_quote[0]}\"\n-{author.mention}",
                color=self.bot.get_random_color()
            )
            quote_embed.set_footer(text=f"Quote uploaded by {uploader.nick or uploader.name}")
            await ctx.send(embed=quote_embed)
    
    @quotebook.command(name="save")
    async def save_quote(self, ctx, author:discord.Member, aliases, *, message):
        # Convert a string representation of a list to a list
        aliases = aliases.strip("[]")
        aliases = aliases.replace("'", "")
        aliases = aliases.replace(", ", ",")
        aliases = aliases.split(",")
        
        chdir(f"{self.bot.BASE_DIR}/resources")
        with open("quotes.json", "r") as f:
            quotes = load(f)
        
        for data in list(quotes.values()):
            for alias in aliases:
                if alias in data["aliases"]:
                    await ctx.send(f"A quote already exists with an alias of `{alias}`, please pick a new alias and try again!")
                    return
        
        quotes[message] = {
            "author": author.id,
            "uploaded_by": ctx.author.id,
            "aliases": aliases
        }
        
        with open("quotes.json", "w") as f:
            dump(quotes, f, indent=2)
        chdir(self.bot.BASE_DIR)

        quote_embed = discord.Embed (
            title="Quote has been saved!",
            description=f"> {message}\n-{author.mention}",
            color=self.bot.get_random_color()
        )
        #quote_embed.set_thumbnail(url=author.avatar_url)
        quote_embed.set_footer(text=f"Quote uploaded by: {ctx.author.nick or ctx.author.name}")

        await ctx.send(embed=quote_embed)
    
    @quotebook.command(name="delete")
    async def delete_quote(self, ctx, alias):
        chdir(f"{self.bot.BASE_DIR}/resources")
        with open("quotes.json", "r") as f:
            quotes = load(f)
        
        fetched_quote = None
        for quote, data in quotes.items():
            if alias in data["aliases"]:
                fetched_quote = [quote, data]
                del quotes[quote]
                break

        if fetched_quote is None:
            await ctx.send(f"No quote was found under the alias `{alias}`, please check your spelling and try again!")
            return
        
        author = get(self.bot.get_all_members(), id=fetched_quote[1]["author"])
        
        with open("quotes.json", "w") as f:
            dump(quotes, f, indent=2)
        chdir(self.bot.BASE_DIR)

        delete_quote_embed = discord.Embed (
            title="Quote has been deleted!",
            description=f"> {fetched_quote[0]}\n-{author.mention}",
            color=self.bot.get_random_color()
        )
        delete_quote_embed.set_footer(text=f"Quote was deleted by: {ctx.author.nick or ctx.author.name}")
        await ctx.send(embed=delete_quote_embed)

def setup(bot):
    bot.add_cog(Quote_Book(bot))