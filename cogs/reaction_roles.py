""" Reaction Role Menu """

# Discord Imports
import discord
from discord.ext import commands
from discord.ext.commands import Greedy

# Other Imports
from emoji import emojize
from json import load, dump
from os import chdir


class Reaction_Roles(commands.Cog, name="Reaction Roles"):
    def __init__(self, bot):
        self.bot = bot
    

    async def load_role_menus(self):
        # Load all role menus from the role_menus.json file and save them as an attribute
        self.role_menus = {}

        chdir(f"{self.bot.BASE_DIR}/resources")
        with open("role_menus.json", "r") as f:
            menu_data = load(f)

        for id, data in menu_data.items():
            # Save the key as a discord message object
            channel_id, message_id = id.split("-")
            channel = self.bot.get_channel(int(channel_id))
            message = await channel.fetch_message(int(message_id))

            role_emoji_dict = {}
            # Convert role ids to discord role objects
            for emoji, role_id in data.items():
                role = channel.guild.get_role(int(role_id))
                emoji = emojize(emoji)
                role_emoji_dict[emoji] = role

            self.role_menus[message] = role_emoji_dict
        chdir(self.bot.BASE_DIR)

    
    @commands.Cog.listener()
    async def on_ready(self):
        await self.load_role_menus()

    # Create a role menu
    @commands.command (
        brief="Creates a role menu.",
        description="Creates an embed where users can add reactions to recieve roles.",
        aliases=["rr_add", "rr_create"]
    )
    @commands.has_permissions(manage_roles=True)
    async def create_role_menu(self, ctx, menu_name, roles: Greedy[discord.Role], *, emojis):
        emojis = emojis.split(" ")

        if len(roles) != len(emojis):
            await ctx.send(f"The number of roles is not the same as the number of emojis, please try again. \n`Role  Count: {len(roles)}`\n`Emoji Count: {len(emojis)}`")
            return
    
        role_menu = discord.Embed (
            title=menu_name.replace("_"," "),
            description="",
            color=self.bot.get_random_color()
        )
        role_emoji_dict = {}
        for role, emoji in zip(roles, emojis):
            role_menu.add_field (
                name=role,
                value=emoji,
                #inline=False
            )
            role_emoji_dict[emoji] = role.id
        role_menu_message = await ctx.send(embed=role_menu)
        for emoji in emojis:
            await role_menu_message.add_reaction(emoji)

        chdir(f"{self.bot.BASE_DIR}/resources")
        with open("role_menus.json", "r") as f:
            menus = load(f)
        menus[f"{str(role_menu_message.channel.id)}-{str(role_menu_message.id)}"] = role_emoji_dict

        with open("role_menus.json", "w") as f:
            dump(menus, f, indent=2)
        chdir(self.bot.BASE_DIR)

        await self.load_role_menus()
    
    # Delete a role menu
    @commands.command (
        brief="Deletes a role menu.",
        description="Deletes a role menu message and removes its data.",
        aliases=["rr_remove", "rr_rmv"]
    )
    @commands.has_permissions(manage_roles=True)
    async def role_menu_remove(self, ctx, *, id):
        if "-" in id:
            channel_id, message_id = id.split("-")
        else:
            channel_id = id[0]
            message_id = id[1]

        chdir(f"{self.bot.BASE_DIR}/resources")
        with open("role_menus.json", "r") as f:
            menus = load(f)
        
        try:
            # Check if a role menu under channel_id-message_id exists
            menus[f"{channel_id}-{message_id}"]

        except KeyError:
            # Wrong channel/message id(s)
            saved_ids = "\n".join(list(menus.keys()))
            await ctx.send(f"There is not a registered role menu under `{channel_id}-{message_id}`. The following is a list of all currently saved menus. \n```{saved_ids}\n```")

        else:
            # Role menu with the id exists
            del menus[f"{channel_id}-{message_id}"]
            await ctx.send(f"Role menu with the id of `{channel_id}-{message_id}` has been successfully deleted.")
        
            channel = self.bot.get_channel(int(channel_id))
            message = await channel.fetch_message(int(message_id))

            
            with open("role_menus.json", "w") as f:
                dump(menus, f, indent=2)
            chdir(f"{self.bot.BASE_DIR}/resources")

            await message.delete()
            await self.load_role_menus()

    # Listeners to add/remove the roles
    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        if payload.member.bot:
            return

        for message in self.role_menus.keys():
            if payload.message_id == message.id:
                if payload.emoji.is_custom_emoji():
                    emoji_name = f"<:{payload.emoji.name}:{payload.emoji.id}>"
                else:
                    emoji_name = payload.emoji.name
                role = self.role_menus[message][emoji_name]
                await payload.member.add_roles(role)
    
    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        guild = self.bot.get_guild(payload.guild_id)
        member = guild.get_member(payload.user_id)

        if member.bot:
            return

        for message in self.role_menus.keys():
            if payload.message_id == message.id:
                if payload.emoji.is_custom_emoji():
                    emoji_name = f"<:{payload.emoji.name}:{payload.emoji.id}>"
                else:
                    emoji_name = payload.emoji.name
                role = self.role_menus[message][emoji_name]
                await member.remove_roles(role)


def setup(bot):
    bot.add_cog(Reaction_Roles(bot))