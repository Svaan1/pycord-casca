import discord
from discord.ext import commands
from utils.sql_handler import Economy_Table


class Economy(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.database = Economy_Table()

    @discord.slash_command(description="Returns an user's (you as default) amount of money")
    async def check_balance(self, ctx, user: discord.Option(discord.Member, required=False)):
        if user:
            user = user.id
        else:
            user = ctx.author.id
        user = self.database.query_user(user)
        await ctx.respond(user.money)

    @discord.slash_command(description="Gives your money to someone else (you're brave.)")
    async def give_money(self, ctx, receiver: discord.Option(discord.Member), value: discord.Option(int)):
        giver = ctx.author.id
        receiver = receiver.id

        if self.database.query_user(giver).money < value:
            return await ctx.respond("Hey, you dont have that much!")
        else:
            # Ok, this is dangerous, i should implement a way to only apply changes if both operations are done
            self.database.subtract_money(giver, value)
            self.database.add_money(receiver, value)
            return await ctx.respond("Done!")


def setup(bot):
    bot.add_cog(Economy(bot))
