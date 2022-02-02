# Discord Imports
import discord
from discord.ext import commands

# Utils
from utils import Utils

# Other Imports
from datetime import datetime
from enum import Enum


class EmbedColor(Enum):
    """Container for Embed Colors"""
    # Message Related Colors
    MESSAGE_SEND = 0x5fe468    # Green
    MESSAGE_EDIT = 0xe6852b    # Orange
    MESSAGE_DELETE = 0xf84b51  # Red


def create_embed(
        *,
        title: str = None,
        description: str = None,
        footer: str = None,
        color: EmbedColor,
        author: discord.Member
) -> discord.Embed:
    embed = discord.Embed(
        title=title or "",
        description=description or "",
        color=color.value,
        timestamp=datetime.now()
    )
    embed.set_author(
        name=str(author),
        icon_url=author.avatar_url
    )
    if footer:
        embed.set_footer(text=footer)
    return embed


def clean_msg(message: str) -> str:
    """Clean up messages with line breaks"""
    return message.replace("\n", "\n> ")


def check_channel(channel_id: int) -> bool:
    """Returns True if a given channel id is a list of channels to ignore logging in"""
    return channel_id in [937444414324887572, 937924972695941171, 937900839400513576, 938246207879381012]


class Logger(commands.Cog):
    """Server Logger"""

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.guild.id != 937426313998917692:
            return

        if check_channel(message.channel.id):
            return

        desc = f"""**Channel:**\n> {message.channel.mention}\n{"-" * 61}\n"""

        if message.reference:
            # Include the original message if the message is a reply
            ref = message.reference
            channel = message.guild.get_channel(ref.channel_id)
            msg = await channel.fetch_message(ref.message_id)
            desc += f"""**__Reply To__**
**Message:**
> {clean_msg(msg.content) or "`None`"}
> - {msg.author.mention}\n{"-" * 61}"""

        desc += f"""**Message:**
> {clean_msg(message.content) or "`None`"}
> - {message.author.mention}"""
        desc += f"\n\n[Jump To Message]({message.jump_url})"

        embed = create_embed(
            title="A Message was Sent",
            description=desc,
            footer=f"Message ID: {message.id}",
            color=EmbedColor.MESSAGE_SEND,
            author=message.author
        )
        if message.attachments:
            if len(message.attachments) == 1:
                embed.set_image(url=message.attachments[0])
                await self.bot.log_channel.send(embed=embed)
            else:
                await self.bot.log_channel.send(
                    embed=embed,
                    files=[await atchmnt.to_file() for atchmnt in message.attachments]
                )
        else:
            await self.bot.log_channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        if message.guild.id != 937426313998917692:
            return

        if check_channel(before.channel.id):
            return

        if before.content == after.content:
            return

        embed = create_embed(
            title="A Message was Edited",
            description=f"""**Channel:**
> {before.channel.mention}
{"-" * 61}
**Before:**
> {clean_msg(before.content) or "`None`"}
> - {before.author.mention}
{"-" * 61}
**After:**
> {clean_msg(after.content) or "`None`"}
> - {after.author.mention}

[Jump To Message]({before.jump_url})
""",
            footer=f"Message ID: {before.id}",
            color=EmbedColor.MESSAGE_EDIT,
            author=before.author
        )
        await self.bot.log_channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        if message.guild.id != 937426313998917692:
            return

        if check_channel(message.channel.id):
            return

        embed = create_embed(
            title="A Message was Deleted",
            description=f"""**Channel:**
> {message.channel.mention}
{"-" * 61}
**Message:**
> {clean_msg(message.content) or "`None`"}
> - {message.author.mention}""",
            footer=f"Message ID: {message.id}",
            color=EmbedColor.MESSAGE_DELETE,
            author=message.author
        )

        if message.attachments:
            if len(message.attachments) == 1:
                embed.set_image(url=message.attachments[0])
                await self.bot.log_channel.send(embed=embed)
            else:
                await self.bot.log_channel.send(
                    embed=embed,
                    files=[await atchmnt.to_file() for atchmnt in message.attachments]
                )
        else:
            await self.bot.log_channel.send(embed=embed)


def setup(bot):
    bot.add_cog(Logger(bot))
