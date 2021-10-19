# Discord Imports
import discord
from discord.ext import commands, tasks

# Other Imports
import datetime as dt
from json import load
import pytz


class LGBT_Days(commands.Cog):
    """ Announcements for LGBT Days """
    def __init__(self, bot):
        self.bot = bot
        self.check_for_event.start()
    
    def get_current_event(self, date):
        """ Returns the lgbt with a given date, or None if there is no saved event """
        with open(f"{self.bot.BASE_DIR}/resources/lgbt_days.json", "r") as f:
            return load(f).get(date)
    

    @tasks.loop(hours=24)
    async def check_for_event(self):
        await self.bot.wait_until_ready()

        curr_date = "-".join(str(dt.date.today()).split("-")[1:]) # get the date in "month-day" format
        todays_events = self.get_current_event(curr_date)

        if todays_events is None:
            # No event scheduled for today
            return
        
        lgbt_days_channel = self.bot.get_guild(844325997566099497).get_channel(898997234115412040)
        if isinstance(todays_events, list):
            # Multiple events on the same day
            description = f"Today is **{todays_events[0]['name']}**"
            for event in todays_events[1:]:
                description += f" and **{event['name']}**"
            """description += "!\n\n"
            
            for message in todays_events:
                if todays_events:
                    pass"""
        
        else:
            # Only one event
            description = f"Today is **{todays_events['name']}**! \n\n{todays_events.get('message', '')}"

        day_embed = discord.Embed (
            description=description,
            color=self.bot.get_random_color()
        )
        await lgbt_days_channel.send(embed=day_embed)

    @check_for_event.before_loop
    async def wait_until_midnight():
        now = dt.datetime.now(pytz.timezone("US/Central"))
        next_run = now.replace(hour=0, minute=0, second=0)

        if next_run < now:
            next_run += dt.timedelta(days=1)
        await discord.utils.sleep_until(next_run)


def setup(bot):
    bot.add_cog(LGBT_Days(bot))