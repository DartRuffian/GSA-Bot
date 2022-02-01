# Discord Imports
import discord
from discord.ext import commands
from discord.ext.commands import Greedy

# Other Imports
from datetime import datetime, timedelta
import asyncio

from discord.ext.commands.core import has_permissions


class Moderation(commands.Cog, name="Mod Only"):
    """Mod-Specific Commands"""
    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        brief="Either deletes a certain number of messages or deletes messages until a certain message is reached.",
        description="""Giving a number of messages to delete will delete that many messages.
Giving a message id will delete all messages in that message's channel and stop after the message is deleted (100 max).
Running the command and not specifying a limit or a message, will send a list of all tags.""",
        aliases=["delete", "del", "clear", "cleanup"]
    )
    @commands.has_permissions(manage_messages=True)
    async def purge(self, ctx, limit: Greedy[int], clear_until: Greedy[discord.Message], *, args="--ip"):
        if limit == [] and clear_until == []:
            # Neither is passed, use as a pseudo help command
            args_desc = {
                "--ip": "Ignore pinned messages. (Default)",
                "--ib": "Ignore bot messages.",
                "--content `<text>`": "Will only delete messages that contain the given text."
            }
            embed = discord.Embed(
                description="Here's a list of all possible arguments and what they do.",
                color=self.bot.transparent_color
            )
            for tag, meaning in args_desc.items():
                embed.add_field(
                    name=tag,
                    value=meaning
                )
            await ctx.send(embed=embed)
            return

        await ctx.message.delete()
        args = [i.strip(" ") for i in args.split("--")[1:]]  # get arguments as a list
        deleted_messages = {}
        text_to_clear = None
        if limit:
            async for message in ctx.channel.history(limit=limit[0]):
                delete_message = True
                # Check the message against the given arguments
                if "ip" in args and message.pinned:
                    delete_message = False
                if "ib" in args and message.author.bot:
                    delete_message = False
                if "content" in str(args):
                    for tag in args:
                        if tag.startswith("content"):
                            text_to_clear = tag[len("content "):].lower()  # get only the text
                    if text_to_clear not in message.content.lower():
                        delete_message = False
                
                if delete_message:
                    count = deleted_messages.get(message.author, 0)
                    count += 1
                    deleted_messages.update({message.author: count})
                    await message.delete()

        elif clear_until:
            async for message in clear_until[0].channel.history(limit=100):
                count = deleted_messages.get(message.author, 0)
                count += 1
                deleted_messages.update({message.author: count})
                await message.delete()
                if message == clear_until[0]:
                    break
        deleted = sum(deleted_messages.values())
        messages = [
            f"""{f'*Only messages containing `{text_to_clear}` were deleted*"' if text_to_clear is not None else ""}
{deleted} message{' was' if deleted == 1 else 's were'} removed."""
        ]
        messages.extend(f"- **{author}**: {count}" for author, count in deleted_messages.items())
        await ctx.send("\n".join(messages), delete_after=10)

    @commands.command(
        aliases=["m"],
        brief="Prevents a user from sending messages.",
        description="Adds a role to the given member that prevents them from sending messages."
    )
    @commands.has_permissions(manage_roles=True)
    async def mute(self, ctx, target: discord.Member, *, reason=None):
        mute_role = ctx.guild.get_role(937444718873284618)
        if mute_role in ctx.author.roles:
            await ctx.send(f"User `{target}` is already muted.")
            return
        await target.add_roles(mute_role, reason=reason)
        await ctx.send(f"User {target} has been muted for the following reason: `{reason}`")

        logging_channel = self.bot.guild.get_channel(937924972695941171)
        mute_embed = discord.Embed(
            description=f"""`{target.display_name}` has been muted by **{ctx.author}**
[Jump to Message]({ctx.message.jump_url})

Reason:
> {reason}""",
            timestamp=datetime.utcnow(),
            color=0x5fe468
        )
        mute_embed.set_author(
            name=self.bot.user, 
            icon_url=self.bot.user.avatar_url
        )
        mute_embed.set_footer(text=f"Role ID: {mute_role.id}")
        await logging_channel.send(embed=mute_embed)
    
    @commands.command(
        aliases=["u"],
        brief="Unmutes a user",
        description="Unmutes a user, run the help command for `mute` for more info."
    )
    @commands.has_permissions(manage_roles=True)
    async def unmute(self, ctx, target: discord.Member, *, reason=None):
        mute_role = ctx.guild.get_role(937444718873284618)
        if mute_role not in ctx.author.roles:
            await ctx.send(f"User `{target}` is not muted.")
            return
        await target.remove_roles(mute_role, reason=reason)
        await ctx.send(f"User {target} has been unmuted for the following reason: `{reason}`")

        logging_channel = self.bot.guild.get_channel(937924972695941171)
        mute_embed = discord.Embed(
            description=f"""`{target.display_name}` has been unmuted by **{ctx.author}**
[Jump to Message]({ctx.message.jump_url})

Reason:
> {reason}""",
            timestamp=datetime.utcnow(),
            color=0xf84b51
        )
        mute_embed.set_author(
            name=self.bot.user, 
            icon_url=self.bot.user.avatar_url
        )
        mute_embed.set_footer(text=f"Role ID: {mute_role.id}")
        await logging_channel.send(embed=mute_embed)

    @commands.command(
        brief="Sends a list of all channels who's last message was sent more than two weeks ago.",
        description="Sends a list of all channels who's last message was sent more than two weeks ago."
    )
    @commands.has_permissions(manage_channels=True)
    async def prune(self, ctx):
        prune_embed = discord.Embed(
            description="""This is a list of all channels who's last message was sent more than two weeks ago.
Channel Name — Days Since Last Message\n\n""",
            color=self.bot.get_random_color()
        )
        async with ctx.channel.typing():
            for channel in ctx.guild.text_channels:
                async for message in channel.history(limit=1):
                    if (datetime.now() - message.created_at) >= timedelta(days=14):
                        days_since_last_message = str(datetime.now() - message.created_at).split(', ')[0]
                        prune_embed.description += f"{channel.mention} — {days_since_last_message}\n"
            await ctx.message.reply(embed=prune_embed)

    '''
    @commands.command(aliases=["va"], hidden=True)
    @has_permissions(administrator=True)
    async def view_anon(self, ctx, message_id):
        admin_channel = self.bot.get_guild(844325997566099497).get_channel(844675657304375300)
        if ctx.channel != admin_channel:
            await ctx.message.delete()
            await ctx.author.send(f"""This command should only be used in {admin_channel.mention} because it reveals 
            private information. Please try again in the proper channel.""")
            return
        
        message_id = message_id.replace("-", "/")
        # Jump urls are stored as guild_id/channel_id/message_id
        # When copying a message id it is saved as channel_id-message_id
        confirm_message = await ctx.send(f"""@everyone
{ctx.author} has requested to look for a private message with the following id: `{message_id}`.
Please have at least two other moderators (and the user who executed the command; so 4 total reactions) approve this.
React with ✅ to confirm this action.""")
        await confirm_message.add_reaction("✅")

        def check_mod_vote(reaction, user):
            return str(reaction.emoji) == "✅" and reaction.count >= 4 and "overseers" in str(user.roles)
        
        try:
            _, _ = await self.bot.wait_for("reaction_add", timeout=60, check=check_mod_vote)
            await ctx.send("Action Approved: Searching for message...")
        except asyncio.TimeoutError:
            await ctx.send("Message has automatically timed out after 60 seconds.")
            return
        
        for channel in self.bot.private_channels:
            async for message in channel.history(limit=30):
                if message.embeds:
                    for description in [embed.description for embed in message.embeds]:
                        if message_id in description:
                            await ctx.send(f"Author: {channel.recipient}\nAuthor ID: `{channel.recipient.id}`")
                            return
        await ctx.send(f"""No messages were found with an id of `{message_id}`. This may be because the private 
        message is no longer cached, which is a limitation from Discord itself. For the message to be re-cached, 
        the author of the original private message will have to send a message to the bot again.""")
    '''


def setup(bot):
    bot.add_cog(Moderation(bot))
