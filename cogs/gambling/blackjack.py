import discord
import asyncio
from discord.ext import commands
from utils.sql_handler import Economy_Table
from games.blackjack import Blackjack


async def players_turn(game, interaction):
    await interaction.response.defer()

    game.player_hit()
    message = interaction.message
    await message.edit(embed=game.embed)

    if game.players_hand.value > 21:
        await end_game(game, message)
    elif game.players_hand.value == 21:
        await dealers_turn(game, interaction)


async def dealers_turn(game, interaction):
    await interaction.response.defer()

    message = interaction.message
    while game.dealers_hand.value < 17 and game.dealers_hand.value < game.players_hand.value:
        game.dealer_hit()
        message = await message.edit(embed=game.embed, view=None)
        await asyncio.sleep(2)
    await end_game(game, message)


async def end_game(game, message):
    result = game.check_result()
    database = Economy_Table()
    user = game.user
    match result:
        case "Player Wins":
            database.add_money(user, game.bet)
        case "Player Loses":
            database.subtract_money(user, game.bet)

    user_balance = database.query_user(user)

    game.embed.add_field(name="Your credits",
                         value=f"You now have {user_balance} credits")
    await message.edit(embed=game.embed, view=None)


class BlackJack(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.database = Economy_Table()

    @discord.slash_command(description="Play BlackJack against our world-renowned dealer (not really)")
    async def blackjack(self, ctx, bet: discord.Option(int, min_value=1)):

        if not self.database.user_has_enough_money(ctx.author.id, bet):
            return await ctx.respond("Hey, you dont have that much!")

        user = ctx.author.id
        game = Blackjack(bet, user)

        class Button_View(discord.ui.View):

            @discord.ui.button(label="Hit", style=discord.ButtonStyle.primary)
            async def hit_button_callback(self, button, interaction):
                if interaction.user.id == user:
                    await players_turn(game, interaction)
                else:
                    await interaction.response.send_message("Hey, thats not for you!", ephemeral=True)

            @discord.ui.button(label="Stand", style=discord.ButtonStyle.primary)
            async def stand_button_callback(self, button, interaction):
                if interaction.user.id == user:
                    await dealers_turn(game, interaction)
                else:
                    await interaction.response.send_message("Hey, thats not for you!", ephemeral=True)

        await ctx.respond(embed=game.embed, view=Button_View())


def setup(bot):
    bot.add_cog(BlackJack(bot))
