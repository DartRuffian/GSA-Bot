# Discord Imports
import discord
from discord.ext import commands

# Other Imports
from datetime import datetime, timedelta

class Moderation(commands.Cog, name="Mod Only"):
    """ Mod-Specific Commands """
    def __init__(self, bot):
        self.bot = bot


    @commands.command (
        aliases=["delete", "del", "cleanup", "clean"],
        brief="Takes a number and deletes that many messages",
        description="Takes an argument `limit` and deletes that many messages from the current channel, optional argument to delete messages that only contain a given phrase."
    )
    @commands.has_permissions(manage_messages=True)
    async def purge(self, ctx, limit: int, *, content_to_delete=None):
        await ctx.message.delete()
        message_count = {}

        async for message in ctx.channel.history(limit=limit):
            if content_to_delete is None or content_to_delete.lower() in message.content.lower():
                if message.author in message_count.keys():
                    message_count[message.author] += 1
                else:
                    message_count[message.author] = 1
                await message.delete()
        
        deleted = sum(message_count.values())
        messages = [f"{f'*Only messages containing the phrase `{content_to_delete}` were deleted*' if content_to_delete is not None else ''}\n{deleted} message{' was' if deleted == 1 else 's were'} removed."]
        messages.extend(f"- **{author}**: {count}" for author, count in message_count.items())
        await ctx.send("\n".join(messages), delete_after=10)
    
    @commands.command (
        aliases=["m"],
        brief="Prevents a user from sending messages.",
        description="Adds a role to the given member that prevents them from sending messages."
    )
    @commands.has_permissions(manage_roles=True)
    async def mute(self, ctx, target: discord.Member, *, reason=None):
        mute_role = ctx.guild.get_role(895855240589492234)
        if mute_role in ctx.author.roles:
            await ctx.send(f"User `{target}` is already muted.")
            return
        await target.add_roles(mute_role, reason=reason)
        await ctx.send(f"User {target} has been muted for the following reason: `{reason}`")

        logging_channel = ctx.guild.get_channel(844690755070328852)
        mute_embed = discord.Embed (
            description=f"`{target.nick or target.name}` has been muted by **{ctx.author}**\n[Jump to Message]({ctx.message.jump_url})\n\nReason:\n> {reason}",
            timestamp=datetime.utcnow(),
            color=0x5fe468
        )
        mute_embed.set_author (
            name=self.bot.user, 
            icon_url=self.bot.user.avatar_url
        )
        mute_embed.set_footer(text=f"Role ID: {mute_role.id}")
        await logging_channel.send(embed=mute_embed)
    
    @commands.command (
        aliases=["u"],
        brief="Unmutes a user",
        description="Unmutes a user, run the help command for `mute` for more info."
    )
    @commands.has_permissions(manage_roles=True)
    async def unmute(self, ctx, target: discord.Member, *, reason=None):
        mute_role = ctx.guild.get_role(895855240589492234)
        if mute_role not in ctx.author.roles:
            await ctx.send(f"User `{target}` is not muted.")
            return
        await target.remove_roles(mute_role, reason=reason)
        await ctx.send(f"User {target} has been unmuted for the following reason: `{reason}`")

        logging_channel = ctx.guild.get_channel(844690755070328852)
        mute_embed = discord.Embed (
            description=f"`{target.nick or target.name}` has been unmuted by **{ctx.author}**\n[Jump to Message]({ctx.message.jump_url})\n\nReason:\n> {reason}",
            timestamp=datetime.utcnow(),
            color=0xf84b51
        )
        mute_embed.set_author (
            name=self.bot.user, 
            icon_url=self.bot.user.avatar_url
        )
        mute_embed.set_footer(text=f"Role ID: {mute_role.id}")
        await logging_channel.send(embed=mute_embed)
    

    @commands.command (
        brief="Sends a list of all channels who's last message was sent more than two weeks ago.",
        description="Sends a list of all channels who's last message was sent more than two weeks ago."
    )
    @commands.has_permissions(manage_channels=True)
    async def prune(self, ctx):
        prune_embed = discord.Embed (
            description="This is a list of all channels who's last message was sent more than two weeks ago. \nChannel Name — Days Since Last Message\n\n",
            color=self.bot.get_random_color()
        )
        async with ctx.channel.typing():
            for channel in ctx.guild.text_channels:
                async for message in channel.history(limit=1):
                    if (datetime.now() - message.created_at) >= timedelta(days=14):
                        prune_embed.description += f"{channel.mention} — {str(datetime.now() - message.created_at).split(', ')[0]}\n"
            await ctx.message.reply(embed=prune_embed)


def setup(bot):
    bot.add_cog(Moderation(bot))