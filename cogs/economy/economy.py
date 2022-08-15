import discord
from utils.sql_handler import Economy_Table

economy = discord.SlashCommandGroup("economy", "Economy related commands")
database = Economy_Table()


@economy.command(name="balance", description="Returns an user's (you as default) amount of money")
async def balance(ctx, user: discord.Option(discord.Member, "Want to check someone else's balance?", required=False)):
    if not user:
        user = ctx.author
    user_balance = database.query_user(user.id).money

    embed = discord.Embed(
        title=f"Balance",
        description=f"{user.mention} has {user_balance} credits",
    )

    await ctx.respond(embed=embed, ephemeral=True)


@economy.command(name="give_money", description="Gives your money to someone else (you're brave.)")
async def give_money(ctx, receiver: discord.Option(discord.Member, "Who shall be the lucky one?"), value: discord.Option(int, "How much are you willing to give?")):
    giver = ctx.author

    if not database.user_has_enough_money(giver.id, value):
        return await ctx.respond("Hey, you dont have that much!")
    else:
        # Ok, this is dangerous, i should implement a way to only apply changes if both operations are done
        database.subtract_money(giver.id, value)
        database.add_money(receiver.id, value)
        return await ctx.respond("Done!", ephemeral=True)


def setup(bot):
    bot.add_application_command(economy)
