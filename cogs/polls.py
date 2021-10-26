# Discord Imports
import discord
from discord.ext import commands
from discord.ext.commands.core import has_permissions

# Other Imports
import asyncio


def to_emoji(i):
    # Convert an int to a letter emoji (0 = A, etc.)
    base = 0x1f1e6
    return chr(base + i)


class Polls(commands.Cog):
    """ Polling Commands """

    def __init__(self, bot):
        self.bot = bot


    @commands.command (
        brief="Creates a simple poll",
        description="Creates a poll with a given question, and uses emojis to count votes"
    )
    async def poll(self, ctx, *, question):
        messages = [ctx.message] # List of messages to delete after creating the poll
        poll_answers = []        # List of answers to the poll

        def check(message):
            return message.author == ctx.author and message.channel == ctx.channel
        
        for i in range(20):
            # Max of 20 reactions, so a max of 20 options
            messages.append(await ctx.send(f"Add poll option or type \"publish\" to publish the poll! "))

            try:
                entry = await self.bot.wait_for("message", check=check, timeout=30.0)
            
            except asyncio.TimeoutError:
                messages.append(await ctx.send("The poll has timed out and has been automatically published"))
                break
            
            messages.append(entry)

            if entry.content.startswith("publish"):
                break

            poll_answers.append((to_emoji(i), entry.clean_content))
        
        await ctx.channel.delete_messages(messages)

        answer = "\n".join(f"{keycap}: {content}" for keycap, content in poll_answers)
        poll_message = await ctx.send(f"{question}\n\n{answer}")
        for emoji, _ in poll_answers:
            await poll_message.add_reaction(emoji)


    @poll.error
    async def poll_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            return await ctx.send("Make sure to include a question to ask when creating a poll!")


def setup(bot):
    bot.add_cog(Polls(bot))