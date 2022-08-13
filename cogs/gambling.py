import random
import discord
from discord.ext import commands
from utils.sql_handler import Economy_Table
from games.blackjack import Blackjack


class Gambling(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.database = Economy_Table()

    @discord.slash_command(description="Toss a coin and maybe gain some")
    async def coinflip(self, ctx, bet: discord.Option(int, "How much you wanna bet?", min_value=1), guess: discord.Option(str, "Head or Tails?", choices=["Heads", "Tails"])):
        if not self.database.user_has_enough_money(ctx.author.id, bet):
            return await ctx.respond("Hey, you dont have that much!")

        coinflip_result = random.choice(["Heads", "Tails"])
        victory = coinflip_result == guess

        embed = discord.Embed(
            title="Coinflip",
            description=f"Flipped a coin, we got **{coinflip_result}!**"
        )

        if victory:
            new_balance = self.database.add_money(ctx.author.id, bet)
            embed_message = f"Nice, you won {bet} credits!"
            embed.color = discord.Colour.green()
        else:
            new_balance = self.database.subtract_money(ctx.author.id, bet)
            embed_message = f"Oh no, you lost {bet} credits..."
            embed.color = discord.Colour.red()

        embed.add_field(
            name=embed_message, value=f"You now got {new_balance} credits")

        await ctx.respond(embed=embed)

    @discord.slash_command(description="To be a poker command")
    async def blackjack(self, ctx):
        game = Blackjack()
        embed = discord.Embed(
            title="Blackjack"
        )
        embed.add_field(name="Your hand",
                        value=f"{game.players_hand}", inline=True)
        embed.add_field(name="Dealer's hand",
                        value=f"{game.dealers_hand}", inline=True)

        await ctx.respond(embed=embed)


def setup(bot):
    bot.add_cog(Gambling(bot))
