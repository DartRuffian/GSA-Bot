# Discord Imports
import discord
from discord.ext import commands


def create_embed(message, member, color) -> discord.Embed:
    """Creates an embed with a given message, color, and thumbnail"""
    embed = discord.Embed(
        description=message,
        color=color
    )
    embed.set_thumbnail(url=member.avatar_url)
    embed.set_footer(text=f"Member Count: {member.guild.member_count}")
    return embed


def get_welcome_channel(guild: discord.Guild) -> discord.TextChannel:
    for channel in guild.text_channels:
        if "welcome" in channel.name.lower():
            return channel


class AutoWelcomer(commands.Cog):
    """Auto Welcomer"""

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member):
        welcome_channel = get_welcome_channel(member.guild)
        if welcome_channel is not None:
            welcome_embed = create_embed(
                f"Everyone please welcome {member.mention} to {member.guild.name}!",
                member,
                0x1dfd00
            )
            await welcome_channel.send(embed=welcome_embed)
            await member.send("""Welcome to the official **GSA Discord Server for Spring Hill**!
Make sure to read up on our rules in <#937426709492408320> and introduce yourself in <#937429290612580472>.
You can also customize your roles in <#937429249831354378> and pick whatever applies to you.

Check out <#937427207796699166> if you ever get lost, it has tons of useful links for you!
Ever miss a meeting? Look at what you missed out on in <#937426750483345428>!""")

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        welcome_channel = get_welcome_channel(member.guild)
        if welcome_channel is not None:
            welcome_embed = create_embed(
                f"Sorry to see you go {member.mention}, hope to see you again!",
                member,
                0xFF0000
            )
            welcome_embed.add_field(
                name="Roles",
                value=", ".join([role.mention for role in member.roles])
            )
            await welcome_channel.send(embed=welcome_embed)


def setup(bot):
    bot.add_cog(AutoWelcomer(bot))
