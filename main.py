from random import randrange


class Card:
    def __init__(self, suit, rank, value):
        self.suit = suit
        self.rank = rank
        self.value = value


class Player:
    bet = 0
    hand = []
    alive = True

    def __init__(self, name, balance):
        self.name = name
        self.balance = balance


def handValue(hand):
    total = 0
    for card in hand:
        total += card.value
    return total


def settle():
    pass


# Print statements
print1 = ". Will you hit, stand, or double down?"
print2 = ". Will you hit or stand?"

if __name__ == '__main__':
    # Set number of decks, percent of cards before shuffle, minimum bet
    decks = int(input("Enter number of decks (1-8 usually): "))
    while decks < 1:
        decks = int(input("Number of decks must be more than 0. Please enter number of decks again: "))

    shufflePercent = int(input("Enter percent of deck you would like to go through before reshuffling: "))
    while shufflePercent < 10 or shufflePercent > 100:
        shufflePercent = int(input("Enter percent between 10 and 100 please: "))
    shufflePercent = float(1-shufflePercent/100)

    minBet = int(input("Enter minimum bet for each hand: "))
    while minBet < 1:
        minBet = int(input("Minimum bet must be more than 0. Please enter minimum bet again: "))

    # List of cards
    fullDeck = []
    # Suits to enumerate
    suits = ["spades", "clubs", "hearts", "diamonds"]

    # Loop for each deck
    for i in range(0, decks):
        # Loop for each suit
        for j in range(0, 4):
            currSuit = suits[j]
            fullDeck.append(Card(currSuit, "ace", 1))
            for k in range(2, 11):
                fullDeck.append(Card(currSuit, str(k), k))
            fullDeck.append(Card(currSuit, "jack", 10))
            fullDeck.append(Card(currSuit, "queen", 10))
            fullDeck.append(Card(currSuit, "king", 10))

    # Copy fullDeck to cardPool so we can reuse fullDeck
    cardPool = fullDeck.copy()

    # Set up players
    players = []
    numPlayers = int(input("Enter number of players (less than 7 is best): "))
    while numPlayers < 1:
        numPlayers = int(input("Enter number of players that is at least 1: "))
    print("\nEnter player information for all players.")
    for i in range(1, numPlayers+1):
        playerName = input("Enter name of player " + str(i) + ": ")
        playerBalance = int(input("Enter balance for " + playerName + ": "))
        while playerBalance < 1:
            print("You're going to want some chips to bet " + playerName + "!")
            playerBalance = int(input("Enter balance more than 0 for " + playerName + ": "))
        players.append(Player(playerName, playerBalance))

    print("\nWelcome to blackjack, best of luck!\n")
    dealerHand = []
    # Main game loop
    while 1:
        # Make sure enough cards remain before next shuffle, reshuffle if not
        if decks*52*shufflePercent+3*(numPlayers+1) > len(cardPool):
            print("Reshuffling cards")
            cardPool = fullDeck.copy

        # Have players place bets
        for i in range(0, numPlayers):
            playerBet = int(input(players[i].name + ", enter your bet: "))
            while playerBet > players[i].balance or playerBet < minBet:
                if playerBet > players[i].balance:
                    playerBet = int(input(players[i].name + ", that exceeds your balance of " + str(players[i].balance)
                                          + ". Enter a bet that doesn't exceed your balance: "))
                elif playerBet < minBet:
                    playerBet = int(input(players[i].name + ", that doesn't meet the minimum bet of " + str(minBet) +
                                          ". Enter a bet of at least " + str(minBet) + ": "))
            players[i].bet = playerBet

        # Deal cards
        for i in range(0, 2):
            for j in range(0, numPlayers):
                cardNum = randrange(len(cardPool))
                players[j].hand.append(cardPool[cardNum])
                del cardPool[cardNum]
            cardNum = randrange(len(cardPool))
            dealerHand.append(cardPool[cardNum])
            del cardPool[cardNum]

        # Check if dealer has blackjack
        if (dealerHand[0].value == 1 and dealerHand[1].value == 10) or (dealerHand[1].value == 1 and dealerHand[0].value
                                                                        == 10):
            print("Dealer has blackjack.")
            for i in range(0, numPlayers):
                players[i].balance -= players[i].bet

        else:
            # Each player does their actions
            for i in range(0, numPlayers):
                while players[i].alive:
                    # Can only double down on first round
                    if len(players[i].hand) == 2:
                        action = input(players[i].name + ", you have " + str(handValue(players[i].hand)) + print1)
                        while action != "hit" and action != "stand" and action != "double down":
                            action = input("Not a valid action. Choose hit, stand, or double down.")
                        # Double down
                        if action == "double down" and players[i].balance < players[i].bet:
                            action = input("You don't have enough balance to double down. Choose hit or stand.")
                            while action != "hit" and action != "stand":
                                action = input("Not a valid action. Choose hit or stand.")
                        if action == "double down":
                            players[i].bet *= 2
                            cardNum = randrange(len(cardPool))
                            players[i].hand.append(cardPool[cardNum])
                            print(players[i].hand[-1].rank + " of " + str(players[i].hand[-1].suit))
                            del cardPool[cardNum]
                            players[i].alive = False
                            break

                    # Get hit or stand actions after first turn
                    if len(players[i].hand) != 2:
                        action = input(players[i].name + ", you have " + str(handValue(players[i].hand)) + print2)
                        while action != "hit" and action != "stand":
                            action = input("Not a valid action. Choose hit or stand.")
                    # Hit
                    if action == "hit":
                        cardNum = randrange(len(cardPool))
                        players[i].hand.append(cardPool[cardNum])
                        print(players[i].hand[-1].rank + " of " + str(players[i].hand[-1].suit))
                        del cardPool[cardNum]
                        if handValue(players[i].hand) > 21:
                            players[i].alive = False
                            print("Bust!")
                    # Stand
                    else:
                        players[i].alive = False

            settle()
            # TODO print balances or something

            cont = input("Play another hand? (y/n)")
            if cont == "n":
                break

            # Remove players that are out
            playersOut = []
            for i in range(0, numPlayers):
                if players[i].balance < minBet:
                    print(players[i].name + ", you can't make the minimum bet with your balance. You're out!")
                    playersOut.append(i)
            for i in range(0, len(playersOut)):
                del players[playersOut[i]]
