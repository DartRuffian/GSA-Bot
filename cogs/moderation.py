# Discord Imports
import discord
from discord.ext import commands


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
    async def mute(self, ctx, target: discord.Member, *, reason=None):
        mute_role = ctx.guild.get_role(895855240589492234)
        await target.add_roles(mute_role, reason=reason)
        await ctx.send(f"User {target} has been muted for the following reason: `{reason}`")
    
    @commands.command (
        aliases=["u"],
        brief="Unmutes a user",
        description="Unmutes a user, run the help command for `mute` for more info."
    )
    async def unmute(self, ctx, target: discord.Member, *, reason=None):
        mute_role = ctx.guild.get_role(895855240589492234)
        await target.remove_roles(mute_role, reason=reason)
        await ctx.send(f"User {target} has been unmuted for the following reason: `{reason}`")


def setup(bot):
    bot.add_cog(Moderation(bot))