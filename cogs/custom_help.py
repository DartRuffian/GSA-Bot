# Discord Imports
import discord
from discord.ext import commands

# Other Imports
from itertools import cycle

class Help_Command(commands.HelpCommand):
    """ Custom Help Command """
    def get_command_signature(self, command):
        return f"{self.clean_prefix}{command.qualified_name} {command.signature}"

    async def send_bot_help(self, mapping):
        color_characters = cycle([
            ("```diff\n-" , "\n```"),
            ("```css\n["  , "]\n```"),
            ("```fix\n"   , "\n```"),
            ("```bash\n\"", "\"\n```"),
            ("```diff\n+" , "\n```"),
        ])

        help_embed = discord.Embed (
            title="Help | General",
            description="",
            color=self.bot.transparent_color
        )
        help_embed.description += "**__Basic Info__:**\nGSA stands for \"Gender and Sexuality Association\" and is an open place for all LGBT+ members and allies to have a good time together!\n\n**__Commands:__**\n"
        for cog, commands in mapping.items():
            filtered = await self.filter_commands(commands)
            command_signatures = [self.get_command_signature(c) for c in filtered]

            if command_signatures:
                cog_name = getattr(cog, "qualified_name", "No Category")
                for command_sig in command_signatures:
                    i = command_signatures.index(command_sig)
                    command_signatures[i] = f"• `{command_sig.strip(' ')}` — {commands[i].brief or 'No information given.'}\n"
                
                current_colors = next(color_characters)
                help_embed.description += f"{current_colors[0]}{cog_name}{current_colors[1]}\n" + "".join(command_signatures)
            
        channel = self.get_destination()
        await channel.send(embed=help_embed)

    async def send_command_help(self, command):
        help_embed = discord.Embed (
            title=f"Help | Command: {command.name}",
            description=(command.description or "No information given.") + "\n\n",
            color=self.bot.transparent_color
        )
        help_embed.description += f"Usage: `{self.get_command_signature(command)}`\n"
        help_embed.set_footer(text="Note: Angle brackets, <>, represent a *required* argument, while regular brackets, [], represent an *optional* argument")
        if command.aliases:
            help_embed.description += f"Command Aliases: {', '.join(f'`{self.clean_prefix}{x}`' for x in command.aliases)}"

        channel = self.get_destination()
        await channel.send(embed=help_embed)
    
    async def send_group_help(self, group):
        help_embed = discord.Embed (
            title=f"Help | Group: {group.qualified_name}",
            description=(group.description or "No information given.") + "\n\n",
            color=self.bot.transparent_color
        )

        for command in group.commands:
            help_embed.description += f"• `{command}` — {command.brief}\n"
        
        help_embed.description += f"\nUsage: `{self.clean_prefix}{group.full_parent_name or group.name} <subcommand>` followed by that subcommand's arguments.\n"
        if group.aliases:
            help_embed.description += f"Group Aliases: {', '.join(f'`{self.clean_prefix}{x}`' for x in group.aliases)}"

        channel = self.get_destination()
        await channel.send(embed=help_embed)
    
    async def send_cog_help(self, cog):
        help_embed = discord.Embed (
            title=f"Help | Cog: {cog.qualified_name}",
            description=f"{cog.description}\n\nList of Commands:\n",
            color=self.bot.transparent_color
        )

        for command in cog.get_commands():
            help_embed.description += f"• `{self.clean_prefix}{command}` — {command.brief or 'No information given.'}\n"

        channel = self.get_destination()
        await channel.send(embed=help_embed)


class Help_Cog(commands.Cog, name="Help"):
    """ Custom Help Cog """
    def __init__(self, bot):
        self.bot = bot
        bot.original_help_command = bot.help_command
        bot.help_command = Help_Command(command_attrs={"brief": "Shows this message."})
        bot.help_command.cog = self


def setup(bot):
    bot.add_cog(Help_Cog(bot))