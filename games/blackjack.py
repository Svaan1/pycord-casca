import asyncio
import discord
from deck_of_cards.deck_of_cards import DeckOfCards, Card
from utils.sql_handler import Economy_Table

SUITS = {0: "♠️", 1: "♥️", 2: "♦️", 3: "♣️"}
MAX_GAME_TIME = 120
database = Economy_Table()


class Game_Embed():
    def __init__(self, player_hand, dealer_hand):
        self.player_hand = player_hand
        self.dealer_hand = dealer_hand
        self.embed = self.get_embed()

    def get_embed(self):
        embed = discord.Embed(
            title="Blackjack"
        )
        embed.add_field(
            name="Your hand", value=f"{self.player_hand}", inline=True)
        embed.add_field(name=chr(173), value=chr(173))
        embed.add_field(name="Dealer's hand",
                             value=f"{self.dealer_hand}", inline=True)

        return embed


class Game_View(discord.ui.View):
    def __init__(self, game):
        super().__init__(timeout=MAX_GAME_TIME)
        self.game = game
        self.user = self.game.user

    @discord.ui.button(label="Hit", style=discord.ButtonStyle.success)
    async def hit_button_callback(self, button, interaction):
        await interaction.response.defer()
        if interaction.user.id == self.user:
            await self.game.players_turn()
        else:
            await interaction.response.send_message("Hey, thats not for you!", ephemeral=True)

    @discord.ui.button(label="Stand", style=discord.ButtonStyle.danger)
    async def stand_button_callback(self, button, interaction):
        await interaction.response.defer()
        if interaction.user.id == self.user:
            await self.game.dealers_turn()
        else:
            await interaction.response.send_message("Hey, thats not for you!", ephemeral=True)

    async def on_timeout(self):
        if not self.game.has_ended:
            database.add_money(self.user, self.game.bet)
        await self.game.message.edit_original_message(view=None)


class Hand():
    def __init__(self):
        self.cards = []
        self.value = 0

    def __repr__(self):
        string = ""
        for card in self.cards:
            string += f"**{card['name']}**{card['suit']}"
        return string + f"\n Total:**{self.value}**"

    def add_to_hand(self, cards):
        for card in cards:
            card_name = card.name[0:2] if card.value == 10 else card.name[0]
            match card_name:
                case "J" | "Q" | "K":
                    self.value += 10
                case "A":
                    if self.value + 11 > 21:
                        self.value += 1
                    else:
                        self.value += 11
                case _:
                    self.value += card.value

            self.cards.append({
                "name": card_name,
                "suit": SUITS[card.suit]
            })


class Blackjack():
    def __init__(self, bet, user):
        self.has_ended = False
        self.user = user
        self.bet = bet
        self.deck = DeckOfCards()
        self.players_hand = Hand()
        self.dealers_hand = Hand()
        self.view = Game_View(game=self)
        self.initial_draw()
        self.update_embed()

    def update_embed(self):
        self.embed = Game_Embed(self.players_hand, self.dealers_hand).embed

    def hit(self, hand: Hand, number_of_cards):
        cards = [self.deck.give_random_card()
                 for _ in range(number_of_cards)]

        hand.add_to_hand(cards)
        self.update_embed()

    def initial_draw(self):
        self.hit(self.players_hand, 2)
        self.hit(self.dealers_hand, 1)

    def player_hit(self):
        self.hit(self.players_hand, 1)

    async def players_turn(self):
        self.player_hit()
        await self.message.edit_original_message(embed=self.embed)
        if self.players_hand.value > 21:
            await self.end_game()
        elif self.players_hand.value == 21:
            await self.dealers_turn()

    def dealer_hit(self):
        self.hit(self.dealers_hand, 1)

    async def dealers_turn(self):
        while self.dealers_hand.value < 17 and self.dealers_hand.value < self.players_hand.value:
            self.dealer_hit()
            await self.message.edit_original_message(embed=self.embed, view=None)
            await asyncio.sleep(2)
        await self.end_game()

    def check_result(self):
        player = self.players_hand.value
        dealer = self.dealers_hand.value

        def dealer_wins():
            self.result = "Player Loses"
            self.color = discord.Colour.from_rgb(225, 6, 0)  # red

        def player_wins():
            self.result = "Player Wins"
            self.color = discord.Colour.from_rgb(57, 255, 20)  # green

        def tie():
            self.result = "Tie"
            self.color = discord.Colour.blue()
            self.bet = 0

        if player > 21:
            dealer_wins()
        elif dealer > 21:
            player_wins()
        elif player > dealer:
            player_wins()
        elif dealer > player:
            dealer_wins()
        elif player == dealer:
            tie()

        self.embed.color = self.color
        self.embed.add_field(
            name=self.result, value=f"**{self.bet}** credits", inline=False)
        return self.result

    async def end_game(self):
        if self.check_result() == "Player Wins":
            database.add_money(self.user, self.bet * 2)
        self.has_ended = True
        user_balance = database.query_user(self.user)

        self.embed.add_field(name="Your credits",
                             value=f"You now have {user_balance} credits")
        await self.message.edit_original_message(embed=self.embed, view=None)
