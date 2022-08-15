import random
from turtle import title
import discord
from utils.sql_handler import Economy_Table

gambling = discord.SlashCommandGroup("gambling", "Test your luck")
database = Economy_Table()


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


@gambling.command(description="Testing views")
async def teste(ctx):
    class View(discord.ui.View):
        def __init__(self, embed, timeout=10):
            super().__init__(timeout=timeout)
            self.embed = embed

        @discord.ui.button(label="Timeout test", style=discord.ButtonStyle.blurple)
        async def button_callback(self, button, interaction):
            await interaction.response.send_message("Cicked")

        async def on_timeout(self):
            await self.message.edit(embed=self.embed, view=None)

    embed = discord.Embed(
        title="Testing some things",
        description="Testeee"
    )
    view = View(embed)
    message = await ctx.response.send_message(embed=embed, view=View(embed=embed))
    view.message = message.message
    print(view.message)


def setup(bot):
    bot.add_application_command(gambling)
