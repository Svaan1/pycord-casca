import discord
from discord.ext import commands


class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.slash_command()
    async def hello(self, ctx):
        await ctx.respond("Hi!")

    @discord.message_command()
    async def mad_casca(self, ctx, message: discord.Message):
        await ctx.respond("Ok.", ephemeral=True, delete_after=1)
        await message.reply("don't care")


def setup(bot):
    bot.add_cog(Fun(bot))
