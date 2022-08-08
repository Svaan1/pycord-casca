import discord
from discord.ext import commands

class Gambling(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    async def is_gambling_channel(ctx): 
        return (ctx.channel.type == discord.ChannelType.text) and (ctx.channel.name == "gambling-hub")

    async def clean_chat(self, ctx):
        await ctx.channel.purge(limit=100)

    @commands.command()
    async def setup(self, ctx):
        await ctx.guild.create_text_channel("gambling-hub")

def setup(bot):
    bot.add_cog(Gambling(bot))