# Discord Imports
import discord
from discord.ext import commands


class Welcomer(commands.Cog):
    """Welcomer"""
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member):
        if member.guild == 937426313998917692:
            await member.send("""Welcome to the official **GSA Discord Server for Spring Hill**!
Make sure to read up on our rules in <#937426709492408320> and introduce yourself in <#937429290612580472>.
You can also customize your roles in <#937429249831354378> and pick whatever applies to you.

Check out <#937427207796699166> if you ever get lost, it has tons of useful links for you!
Ever miss a meeting? Look at what you missed out on in <#937426750483345428>!""")


def setup(bot):
    bot.add_cog(Welcomer(bot))
