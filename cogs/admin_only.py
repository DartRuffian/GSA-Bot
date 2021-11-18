# Discord Imports
import discord
from discord.ext import commands

# Eval Imports
from contextlib import redirect_stdout
import traceback
import textwrap
import io

# Uptime Imports
from datetime import datetime


def cleanup_code(content):
    """Removes code blocks from the code"""
    if content.startswith("```") and content.endswith("```"):
        return "\n".join(content.split("\n")[1:-1])


class AdminOnly(commands.Cog):
    """Admin Only commands, generally only meant to be used by the bot author"""
    def __init__(self, bot):
        self.bot = bot
        self._last_result = None

    @commands.command(hidden=True)
    @commands.is_owner()
    async def eval(self, ctx, *, body: str):
        env = {
            "bot": self.bot,
            "ctx": ctx,
            "channel": ctx.channel,
            "author": ctx.author,
            "guild": ctx.guild,
            "message": ctx.message,
            "_": self._last_result
        }

        env.update(globals())

        body = cleanup_code(body)
        stdout = io.StringIO()

        to_compile = f"async def func():\n{textwrap.indent(body, '  ')}"

        try:
            exec(to_compile, env)
        except Exception as e:
            return await ctx.send(f"```py\n{e.__class__.__name__}: {e}\n```")

        func = env["func"]
        try:
            with redirect_stdout(stdout):
                ret = await func()
        except Exception:
            value = stdout.getvalue()
            await ctx.send(f"```py\n{value}{traceback.format_exc()}\n```")
        else:
            value = stdout.getvalue()
            try:
                await ctx.message.add_reaction("\u2705")
            except Exception:
                pass

            if ret is None:
                if value:
                    await ctx.send(f"```py\n{value}\n```")
            else:
                self._last_result = ret
                await ctx.send(f"```py\n{value}{ret}\n```")

    @commands.command()
    async def uptime(self, ctx):
        delta_uptime = datetime.utcnow() - self.bot.launch_time
        hours, remainder = divmod(int(delta_uptime.total_seconds()), 3600)
        minutes, seconds = divmod(remainder, 60)
        days, hours = divmod(hours, 24)
        uptime_embed = discord.Embed(
            description=f"Uptime for **{self.bot.user.name}**: `{days}d, {hours}h, {minutes}m, {seconds}s`",
            color=self.bot.get_random_color()
        )
        await ctx.send(embed=uptime_embed)


def setup(bot):
    bot.add_cog(Admin_Only(bot))
