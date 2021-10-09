# Discord Imports
import discord
from discord.ext import commands

# Other Imports
import itertools as it

"""
class MyHelpCommand(commands.MinimalHelpCommand):
    def get_command_signature(self, command):
        return '{0.clean_prefix}{1.qualified_name} {1.signature}'.format(self, command)

class MyCog(commands.Cog):
    def __init__(self, bot):
        self._original_help_command = bot.help_command
        bot.help_command = MyHelpCommand()
        bot.help_command.cog = self

    def cog_unload(self):
        self.bot.help_command = self._original_help_command
#######
See the documentation: https://discordpy.readthedocs.io/en/latest/ext/commands/api.html#help-commands for more details.
For migrating from old helpformatters: https://discordpy.readthedocs.io/en/latest/migrating.html#helpformatter-and-help-command-changes

A walkthrough on subclassing help: 
https://gist.github.com/InterStella0/b78488fb28cadf279dfd3164b9f0cf96
"""

class Help_Command(commands.HelpCommand):
    """ Custom Help Command """
    def get_command_signature(self, command):
        return f"{self.clean_prefix}{command.qualified_name} {command.signature}"

    async def send_bot_help(self, mapping):
        color_characters = it.cycle([
            ("```diff\n-" , "\n```"),
            ("```css\n["  , "]\n```"),
            ("```fix\n"   , "\n```"),
            ("```bash\n\"", "\"\n```"),
            ("```diff\n+" , "\n```"),
        ])

        help_embed = discord.Embed (
            title="Help | General",
            description="",
            color=0x2F3136
        )
        help_embed.description += "**__Basic Info__:**\nGSA stands for \"Gender and Sexuality Association\" and is an open place for all LGBT+ members and allies to have a good time together!\n\n**__Commands:__**\n"
        for cog, commands in mapping.items():
            filtered = await self.filter_commands(commands)
            command_signatures = [self.get_command_signature(c) for c in filtered]

            if command_signatures:
                cog_name = getattr(cog, "qualified_name", "No Category")
                for i in range(len(command_signatures)):
                    command_signatures[i] = f"- `{command_signatures[i].strip(' ')}` — {commands[i].brief or 'No information given.'}\n"
                
                current_colors = next(color_characters)
                help_embed.description += f"{current_colors[0]}{cog_name}{current_colors[1]}\n" + "".join(command_signatures)
            
        channel = self.get_destination()
        await channel.send(embed=help_embed)

    async def send_command_help(self, command):
        help_embed = discord.Embed (
            title=f"Help: Command | {command.name}",
            description=command.description or "No information given.",
            color=0x2F3136
        )

        if command.aliases:
            aliases = [command.aliases]
            for i in range(len(aliases)):
                aliases[i] = f"`{aliases[i]}`"
            help_embed.description += f"\nCommand Aliases: {', '.join(f'`{self.clean_prefix}{x}`' for x in command.aliases)}"

        channel = self.get_destination()
        await channel.send(embed=help_embed)
    
    async def send_group_help(self, group):
        help_embed = discord.Embed (
            title=f"Help: Group | {group.qualified_name}",
            description="",
            color=0x2F3136
        )

        for command in group.commands:
            help_embed.description += f"`{command}` — {command.brief}\n"
        
        if group.aliases:
            help_embed.description += f"\nGroup Aliases: {', '.join(f'`{self.clean_prefix}{x}`' for x in group.aliases)}"

        channel = self.get_destination()
        await channel.send(embed=help_embed)
    
    # !help <cog>
    async def send_cog_help(self, cog):
        help_embed = discord.Embed (
            title=f"Help: Cog | {cog.qualified_name}",
            description=f"{cog.description}\n\nList of Commands:\n",
            color=0x2F3136
        )

        for command in cog.get_commands():
            help_embed.description += f"- `{self.clean_prefix}{command}`\n"

        channel = self.get_destination()
        await channel.send(embed=help_embed)


class Help_Cog(commands.Cog, name="Help"):
    """ Custom Help Cog """
    def __init__(self, bot):
        self.bot = bot
        bot.original_help_command = bot.help_command
        bot.help_command = Help_Command()
        bot.help_command.cog = self
    
    @commands.command(hidden=True)
    @commands.is_owner()
    async def load(self, ctx):
        self.bot.help_command = Help_Command()

    @commands.command(hidden=True)
    @commands.is_owner()
    async def unload(self, ctx):
        self.bot.help_command = self.bot.original_help_command


def setup(bot):
    bot.add_cog(Help_Cog(bot))