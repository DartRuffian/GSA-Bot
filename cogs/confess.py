# Discord Imports
import discord
from discord.ext import commands

# Other Imports
from utils import Utils
import os
import asyncio

class Confessions(commands.Cog, name="Confessions"):
    """ Anonymous Confessions """
    def __init__(self, bot):
        self.bot = bot


    @commands.command (
        aliases=["ac", "confess", "anon_confess"],
        brief="Makes an anonymous confession",
        description="This command only works in a direct message with the bot, which takes a confession and sends it for you to keep it anonymous. Nothing is recorded."
    )
    @commands.dm_only()
    async def anonymous_confession(self, ctx, *, message):
        guild = self.bot.get_guild(844325997566099497)
        channel_aliases = {
            "anon": 847293323672682506,
            "vent": 894813821133262878,
            "will": 400337254989430784
        }

        def check_trigger_warnings(message):
            return message.author == ctx.author and message.channel == ctx.channel and message.content.lower() in ["cancel", "continue"]
        
        try:
            await ctx.send(f"If your message contains sensitive content, please include trigger warnings at the beginning of your message. \nNote: You can type `{ctx.prefix}trigger list` to get a \"full\" list of triggers. \n\nType `cancel` to cancel the publishing of your message and add trigger warnings to the begining if necessary or `continue` to continue.")
            response = await self.bot.wait_for("message", check=check_trigger_warnings, timeout=30.0)
        
        except asyncio.TimeoutError:
            await ctx.send("Your response has timed out, so no message has been sent.")
            return
        
        if response.content.lower() == "cancel":
            await ctx.send("Your message has been canceled.")
            return


        if "<" in message or ">" in message:
            await ctx.author.send("Note that the angle brackets, the '<' and '>' characters, only mean that the message can be multiple words and aren't required.\n\nFor example, this is a perfectly good example of running the command: \n`$confess You're a cutie`")

        confession_embed = discord.Embed (
            description=message,
            color=self.bot.get_random_color()
        )
        confession_embed.set_footer(text=f"Want to talk about something anonymously? Simply privately message the bot \"{ctx.prefix}ac\" followed by your message.")

        def check_message_target(message):
            return message.author == ctx.author and message.channel == ctx.channel and message.content.lower() in channel_aliases.keys()
        
        try:
            await ctx.send("Would you like your message to be sent to <#894813821133262878>, <#847293323672682506>, or William (DartRuffian)'s private messages? Respond with `vent`, `anon`, or `will` to continue. If you choose to have your message sent to William, please be aware that your discord id will be temporarily saved so that William can respond to it. This information is kept private and deleted once the conversation is over.")
            response = await self.bot.wait_for("message", check=check_message_target, timeout=30.0)
        
        except asyncio.TimeoutError:
            await ctx.send("Your response has timed out, so no message has been sent.")
            return
        
        channel = guild.get_channel(channel_aliases[response.content.lower()]) or self.bot.get_user(channel_aliases[response.content.lower()])

        if response.content.lower() == "will":
            latest_user = os.getenv("latest_confession_id")
            if not latest_user:
                # No current confession going on
                confession = await channel.send(embed=confession_embed)
                await ctx.author.send("Your confession has been recorded.")
                os.environ["latest_confession_id"] = str(ctx.author.id)
                return
                
            elif ctx.author.id == int(latest_user):
                # There is a confession, and with this user
                confession = await channel.send(embed=confession_embed)
                await ctx.author.send("Your confession has been sent!")
            
            else:
                # There is a confession, but not with this user
                await ctx.author.send("Due to William not wanting to permanently log any confessions or user data, private confessions are limited to a single user at a time. Please try again later, and sorry for the inconvience.")

        else:
            confession = await channel.send(embed=confession_embed)
            link_embed = discord.Embed(
                description=f"Your confession has been recorded. \n[You can view your message here.]({confession.jump_url}/ \"Click to jump!\")",
                color=self.bot.transparent_color
            )
            await ctx.author.send(embed=link_embed)
    
    @anonymous_confession.error
    async def confession_error(self, ctx, error):
        if isinstance(error, commands.errors.PrivateMessageOnly):
            await ctx.message.delete()
            await ctx.send("This command can only be used in a private message with the bot, and your message has been deleted so that it won't be seen by other users.", delete_after=3)
            await ctx.author.send("Instead, run the command here.")
        
        elif isinstance(error, commands.errors.MissingRequiredArgument):
            await ctx.message.reply("Looks like you missed an argument there, make sure you type `$confess` (or any other alias for the command) followed by your message.")


        error_channel = self.bot.get_guild(844325997566099497).get_channel(892221441481777202)
        message, error_embed = Utils.create_error_embed(self.bot, ctx.message.content, error)

        await error_channel.send(message or "", embed=error_embed)
        await ctx.send(embed=error_embed)      
    
    @commands.command(hidden=True)
    @commands.is_owner()
    @commands.dm_only()
    async def reply(self, ctx, *, message: str):
        latest_user = os.getenv("latest_confession_id")
        if latest_user is not None:
            latest_user = self.bot.get_user(int(latest_user))
        else:
            await ctx.author.send("There is not a currently active private confession")

        private_embed = discord.Embed (
            description=message + "\n\n- William",
            color=self.bot.get_random_color()
        )
        private_embed.set_footer(text="This is a private confession, to end this conversation, type `$finished` to stop it at any time.")
        await latest_user.send(embed=private_embed)
        await ctx.author.send("Your message has been sent.")
    
    @commands.command(hidden=True, aliases=["finish"])
    @commands.dm_only()
    async def end_private_confession(self, ctx):
        if os.getenv("latest_confession_id") is None:
            await ctx.send("There is currently no private confessions going on, feel free to start one!")

        elif (str(ctx.author.id) == os.getenv("latest_confession_id")) or (str(self.bot.owner_id) == os.getenv("latest_confession_id")):
            del os.environ["latest_confession_id"]
            await ctx.author.send("This private confession has ended, and all saved data has been cleared.")
            bot_owner = self.bot.get_user(self.bot.owner_id)
            await bot_owner.send("This private confession has ended, and all saved data has been cleared.")
        
        else:
            await ctx.send("There is currently another private confession with another user.")
    

    @commands.group (
        brief="Trigger related commands",
        description="If called without a subcommand, the bot will say what a trigger is and *why* trigger warnings are necessary.",
        invoke_without_command=True
    )
    async def trigger(self, ctx):
        trigger_embed = discord.Embed (
            description="> \"A trigger is something that sets off a memory tape or flashback transporting the person back to the event of her/his original trauma.\"\n- PsychCentral (<https://psychcentral.com/lib/what-is-a-trigger>) \n\nTriggers are very personal and are most commonly activated by sight and sound. So please be considerate when discussing topics that may make others uncomfortable.",
            color=self.bot.transparent_color
        )
        await ctx.send(embed=trigger_embed)

    @trigger.command (
        name="list",
        brief="Sends a list of possible triggers",
        description="Sends a list of possible triggers and their definitions. Messages that contain these topics **must** have a trigger warning and use spoiler tags."
    )
    async def trigger_list(self, ctx):
        trigger_embed = discord.Embed (
            description="The following is not a full list of triggers, but covers the more common ones that may come up.",
            color=self.bot.transparent_color
        )
        trigger_embed.set_footer(text="In short, if you think something may offend someone, put a trigger warning and put the possibly offensive text in a spoiler.")
        
        possible_triggers = {
            "Suicide": "The act of ending one's own life.",
            "Self Harm": "The act of harming oneself; may be abbreviated to 'sh'.",
            "Sexual Assault": "The act of someone *intentionally* touches someone without that person's consent, or coerces someone to engage in a sexual act without their consent.",
            "Eating Disorders": "Disorders that are related to eating, such as anorexia, binge eating disorder, etc.",
            "Extreme Cases of Homophobia, Transphobia, etc.": "Minor cases of <x>phobia, such as someone being called the f-slur, don't need a trigger warning but the extreme cases will. One example includes ||being told to kill yourself because of your sexuality, gender, etc.||",
            "Abuse": "Someone being physically or psychologically harmed, this includes abuse from family, friends, etc."
        }

        for trigger, definition in possible_triggers.items():
            trigger_embed.add_field (
                name=trigger,
                value=definition
            )
        await ctx.send(embed=trigger_embed)


def setup(bot):
    bot.add_cog(Confessions(bot))