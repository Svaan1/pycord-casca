import discord
from discord.ext import commands


class Events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="você"))
        print('We have logged in as {0.user}'.format(self.bot))

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return


def setup(bot):
    bot.add_cog(Events(bot))
