from deck_of_cards.deck_of_cards import DeckOfCards, Card
SUITS = {0: "♠️", 1: "♥️", 2: "♦️", 3: "♣️"}


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
            card_name = card.name[0]
            self.cards.append({
                "name": card_name,
                "suit": SUITS[card.suit]
            })
            if card_name in ["J", "Q", "K"]:
                self.value += 10
            elif card_name == "A":
                if self.value + 11 > 21:
                    self.value += 1
                else:
                    self.value += 11
            else:
                self.value += card.value


class Blackjack():
    def __init__(self):
        self.deck = DeckOfCards()
        self.players_hand = Hand()
        self.dealers_hand = Hand()
        self.initial_draw()

    def hit(self, hand: Hand, number_of_cards):
        cards = [self.deck.give_random_card()
                 for _ in range(number_of_cards)]

        hand.add_to_hand(cards)

    def initial_draw(self):
        self.hit(self.players_hand, 2)
        self.hit(self.dealers_hand, 1)
