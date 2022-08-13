import discord
from discord.ext import commands
from utils.sql_handler import Economy_Table


class Economy(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.database = Economy_Table()

    @discord.slash_command(description="Returns an user's (you as default) amount of money")
    async def balance(self, ctx, user: discord.Option(discord.Member, "Want to check someone else's balance?", required=False)):
        if not user:
            user = ctx.author
        user_balance = self.database.query_user(user.id).money

        embed = discord.Embed(
            title=f"Balance",
            description=f"{user.mention} has {user_balance} credits",
        )

        await ctx.respond(embed=embed, ephemeral=True)

    @discord.slash_command(description="Gives your money to someone else (you're brave.)")
    async def give_money(self, ctx, receiver: discord.Option(discord.Member), value: discord.Option(int)):
        giver = ctx.author

        if not self.database.user_has_enough_money(giver.id, value):
            return await ctx.respond("Hey, you dont have that much!")
        else:
            # Ok, this is dangerous, i should implement a way to only apply changes if both operations are done
            self.database.subtract_money(giver.id, value)
            self.database.add_money(receiver.id, value)
            return await ctx.respond("Done!")


def setup(bot):
    bot.add_cog(Economy(bot))
