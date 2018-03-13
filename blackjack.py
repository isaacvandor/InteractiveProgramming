import random
from unicards import unicard


class Card:
    """Represents a standard playing card.

    Attributes:
      suit: integer 0-3
      rank: integer 1-13
    """

    suit_names = ["Clubs", "Diamonds", "Hearts", "Spades"]
    rank_names = [None, "Ace", "2", "3", "4", "5", "6", "7",
              "8", "9", "10", "Jack", "Queen", "King"]

    def __init__(self, suit=0, rank=2):
        """Initializes a Card with a suit and rank."""
        self.suit = suit
        self.rank = rank

    def __str__(self):
        """Returns a unicard representation of the Card."""
        suit = self.suit
        rank = self.rank
        return convert_to_unicard(suit,rank)


    def __eq__(self, other):
        """Checks whether self and other have the same rank and suit.

        returns: boolean
        """
        return self.suit == other.suit and self.rank == other.rank

    def __lt__(self, other):
        """Compares this card to other, first by suit, then rank.

        returns: boolean
        """
        t1 = self.suit, self.rank
        t2 = other.suit, other.rank
        return t1 < t2



class Deck:
    """Represents a deck of cards.

    Attributes:
      cards: list of Card objects.
    """

    def __init__(self):
        """Initializes the Deck with 52 cards."""
        self.cards = []
        for suit in range(4):
            for rank in range(1, 14):
                card = Card(suit, rank)
                self.cards.append(card)

    def __str__(self):
        """Returns a string representation of the deck.
        """
        res = []
        for card in self.cards:
            res.append(str(card))
        return ' '.join(res)

    def add_card(self, card):
        """Adds a card to the deck.

        card: Card
        """
        self.cards.append(card)

    def remove_card(self, card):
        """Removes a card from the deck or raises exception if it is not there.

        card: Card
        """
        self.cards.remove(card)

    def pop_card(self, i=-1):
        """Removes and returns a card from the deck.

        i: index of the card to pop; by default, pops the last card.
        """
        return self.cards.pop(i)

    def shuffle(self):
        """Shuffles the cards in this deck."""
        random.shuffle(self.cards)

    def sort(self):
        """Sorts the cards in ascending order."""
        self.cards.sort()

    def move_cards(self, hand, num):
        """Moves the given number of cards from the deck into the Hand.

        hand: destination Hand object
        num: integer number of cards to move
        """
        for i in range(num):
            hand.add_card(self.pop_card())


class Hand(Deck):
    """Represents a hand of playing cards."""

    def __init__(self, label=''):
        self.cards = []
        self.label = label
        self.total = 0


class Game():
    """Represents a game of blackjack"""

    def __init__(self):
        """Starts a new round of blackjack"""
        self.deck=Deck()
        self.deck.shuffle()
        self.player=Hand('Player')
        self.dealer=Hand('Dealer')

    def deal(self):
        """Deals 2 cards to the player and one to the dealer"""
        self.deck.move_cards(self.dealer,1)
        print("Dealer" + str(self.dealer) + " []")
        self.deck.move_cards(self.player,2)
        print("Player" + str(self.player))

    def play(self):
        """Simulates the player's turn in a game of blackjack"""
        ans = input("Would you like to hit or stay?\n")
        if (ans == "hit"):
            self.deck.move_cards(self.player,1)
            print("Player" + str(self.player))
            self.play()
        elif (ans == "stay"):
            total = (self.get_player_total())
            if (total == 'BUST'):
                print("BUST\nDealer Wins")
            else:
                print(self.house())
        else:
            print("Error: End of Game")

    def house(self):
        """Simulates the dealer's turn in a game of blackjack

        returns: String containing the results of the game"""
        self.deck.move_cards(self.dealer,1)
        print("Dealer" + str(self.dealer))
        self.get_dealer_total()

        while(self.dealer.total<=17):
            (self.get_dealer_total())
            if(self.dealer.total>=self.player.total):
                return ("Dealer Wins")
            else:
                self.deck.move_cards(self.dealer,1)
                print("Dealer" + str(self.dealer))
                self.get_dealer_total()

        if(self.dealer.total>21):
            return ("Dealer Bust\n Player Wins")
        elif(self.dealer.total>=self.player.total):
            return ("Dealer Wins")
        return ("Player Wins")

    def get_dealer_total(self):
        """Calculates the current total points of the dealer.

        If there is an ace it will determine whether to be worth 11 or 1 point
        besed on if the current total is less than or equal to 10"""
        values = [None, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10]
        self.dealer.cards.sort(reverse = True)
        self.dealer.total = 0
        for x in self.dealer.cards:
            if x.rank == 1:
                if self.dealer.total<=10:
                    self.dealer.total += 11
                else:
                    self.dealer.total += 1
            else:
                self.dealer.total += values[x.rank]


    def get_player_total(self):
        """Calculates the current total points of the player and gives the
        player the option to choose if an ace counts for 1 point or 11.

        returns: BUST if it is over 21 or it will return the total
        if it is less than 21"""
        values = [None, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10]
        self.player.cards.sort(reverse = True)
        for x in self.player.cards:
            if x.rank == 1:
                ace = int(input("11 or 1 \n"))
                while (ace != 1 and ace != 11):
                    ace = int(input("11 or 1\n"))
                self.player.total += ace
            else:
                self.player.total += values[x.rank]
        if self.player.total > 21:
            return "BUST"
        else:
            return self.player.total



def convert_to_unicard(suit=0, rank=2):
    unicard_suit = ['s','h','d', 'c']
    unicard_rank = [None, 'A','2','3','4','5','6','7','8','9','T','J','Q','K']
    card = str(unicard_rank[rank])+str(unicard_suit[suit])
    return unicard(card)


if __name__ == '__main__':
    round1 = Game()
    round1.deal()
    round1.play()