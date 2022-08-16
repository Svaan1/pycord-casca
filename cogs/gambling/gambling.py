import random
import discord
from games.blackjack import Blackjack
from utils.sql_handler import Economy_Table

gambling = discord.SlashCommandGroup("gambling", "Test your luck")
database = Economy_Table()


# Change this to an object as well :)
@gambling.command(description="Toss a coin and maybe gain some")
async def coinflip(ctx, bet: discord.Option(int, "How much you wanna bet?", min_value=1), guess: discord.Option(str, "Head or Tails?", choices=["Heads", "Tails"])):
    if not database.user_has_enough_money(ctx.author.id, bet):
        return await ctx.respond("Hey, you dont have that much!")

    coinflip_result = random.choice(["Heads", "Tails"])
    victory = coinflip_result == guess

    embed = discord.Embed(
        title="Coinflip",
        description=f"Flipped a coin, we got **{coinflip_result}!**"
    )

    if victory:
        new_balance = database.add_money(ctx.author.id, bet)
        embed_message = f"Nice, you won {bet} credits!"
        embed.color = discord.Colour.from_rgb(57, 255, 20)
    else:
        new_balance = database.subtract_money(ctx.author.id, bet)
        embed_message = f"Oh no, you lost {bet} credits..."
        embed.color = discord.Colour.from_rgb(225, 6, 0)

    embed.add_field(
        name=embed_message, value=f"You now got {new_balance} credits")

    await ctx.respond(embed=embed)


@gambling.command(description="The one closest to 21 wins!")
async def blackjack(ctx, bet: discord.Option(int, min_value=1)):
    if not database.user_has_enough_money(ctx.author.id, bet):
        return await ctx.respond("Hey, you dont have that much!")
    user = ctx.author.id
    database.subtract_money(user, bet)
    game = Blackjack(bet, user)
    game.message = await ctx.response.send_message(embed=game.embed, view=game.view)


def setup(bot):
    bot.add_application_command(gambling)
