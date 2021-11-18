# Discord Imports
from discord.ext import commands
from discord.ext.commands import has_permissions
from discord.utils import get

# Other Imports
from random import choice as rchoice


class SecretSanta(commands.Cog, name="Secret Santa"):
    """Secret Santa event!"""
    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        brief="Starts the Secret Santa event, needs a role named either `Secret Santa` or `secret santa` to begin.",
        desciption="Only a server administrator can start the event."
    )
    @has_permissions(administrator=True)
    async def start(self, ctx):
        event_role = get(ctx.guild.roles, name="Secret Santa") or get(ctx.guild.roles, name="secret santa")
        
        if event_role is None:
            await ctx.send("""There is no role named either "Secret Santa" or "secret santa"."
Please create a role with either of these names before trying again.""")
            return

        event_members = [member for member in ctx.guild.members if event_role in member.roles]
        # get a list of all members who have the event role

        if not event_members:
            await ctx.send(f"""It doesn't seem like anyone has the {event_role.mention} role.
You might want to invite some people first!""")
            return
        elif len(event_members) <= 2:
            await ctx.send(
                "You know you don't need to hold a secret santa for two people to give each other gifts right?"
            )
            return

        for member in event_members:
            # For each person in the event, assign them a random user and remove that random user from the list

            list_copy = event_members  # make a temporary copy of the list
            list_copy.remove(member)   # remove the current member

            rand_member = rchoice(list_copy)   # get a random member, excluding the current member
            event_members.remove(rand_member)  # remove the random member so that they are not "drawn" twice

            await member.send(f"Attention {member.name}! \nYou're assigned Secret Santa is... \n`{rand_member}`!")
        
        await ctx.send(f"{event_role.mention} \nEveryone has been notified of their Secret Santa, let the event begin!")


def setup(bot):
    bot.add_cog(SecretSanta(bot))
