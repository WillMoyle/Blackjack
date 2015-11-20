###############################################################################
##### BLACKJACK SIMULATOR
###############################################################################

# Author: Will Moyle
# Last Modified: 20 Nov 2015

###############################################################################
##### IMPORT STATEMENTS
###############################################################################

import random

###############################################################################
##### GLOBAL VARIABLES
###############################################################################

# values for 52 cards in a standard deck
DECK = [i for i in range(13) for _ in range(4)]

# the names of each of the cards
CARD_NAMES = {
        0: "ACE",
        1: "TWO",
        2: "THREE",
        3: "FOUR",
        4: "FIVE",
        5: "SIX",
        6: "SEVEN",
        7: "EIGHT",
        8: "NINE",
        9: "TEN",
        10: "JACK",
        11: "QUEEN",
        12: "KING"
    }
    
# the names of the various strategies
STRATEGY_NAMES = [
    "Manual",
    "Soft 16",
    "Soft 17",
    "Soft 18",
    "Soft 19",
    "Soft 20",
    "Soft 21",
    "Hard 16",
    "Hard 17",
    "Hard 18",
    "Hard 19",
    "Hard 20",
    "Hard 21"
]

###############################################################################
##### MAIN FUNCTION
###############################################################################

def play_blackjack():
    print "\n*******************************************"    
    welcome_message()
    
    num_hands = 1
    win = 0
    loss = 0
    draw = 0
    hand = 0
    blackjacks = 0
    verbose = True
    winnings = 0
    
    print "\n*******************************************"
    
    output = "What is your strategy going to be? "
    output += "(Manual / Soft 16-21 / Hard 16-21) "
    strategy = raw_input(output)
    while not strategy in STRATEGY_NAMES:
        strategy = raw_input("Invalid input, try again: ")
        
    bet_str = raw_input("How much will you bet each hand? $")
    bet = positive_number(bet_str)
    while bet == -1:
        bet_str = raw_input("Invalid input, try again: $")
        bet = positive_number(bet_str)
        
    multiplier_str = raw_input("Multiplier for Blackjack wins (e.g. 1.5): ")
    multiplier = positive_number(multiplier_str)
    while multiplier_str == -1:
        multiplier_str = raw_input("Invalid input, try again: ")
        multiplier = positive_number(multiplier_str)
        
    soft_str = raw_input("Dealer stands on soft 17's or hard 17's? (S/H) ")
    soft = True if soft_str in ['S', 's'] else False
    
    if strategy != "Manual":
        verb_yn = raw_input("Do you wish to see each hand in detail? (Y/N) ")
        verbose = True if verb_yn in ['Y','y'] else False        
        num_str = raw_input("How many hands do you want to play? ")
        num_hands = natural_number(num_str)
        while num_hands == -1:
            num_str = raw_input("Invalid input, try again: ")
            num_hands = natural_number(num_str)
    
    while num_hands > 0:
        result = play_hand(verbose, soft, strategy)
        hand += 1
        if strategy != "Manual":
            num_hands -= 1
        if result == -1:
            loss += 1
            winnings -= bet
        elif result == 0:
            draw += 1
        elif result == 1:
            win += 1
            winnings += bet
        elif result == 2:
            win += 1
            blackjacks += 1
            winnings += (bet * multiplier)
        if verbose:
            print "\nAfter round " + str(hand) + " the results are:"
            print "Wins: " + str(win)
            print "Draws: " + str(draw)
            print "Losses: " + str(loss)
            print "Blackjack wins: " + str(blackjacks)
            output = "Winnings: "
            if winnings >= 0:
                output += "$" + ("%.2f" % winnings)
            else:
                output += "-$" + ("%.2f" % -winnings)
            print output
            if strategy == "Manual":
                again = raw_input("Do you wish to play another round? (Y/N) ")
                if again in ['Y', 'y']:
                    continue
                else:
                    break
    
    if not verbose:
        print "\nAfter round " + str(hand) + " the results are:"
        print "Wins: " + str(win)
        print "Draws: " + str(draw)
        print "Losses: " + str(loss)
        print "Blackjack wins: " + str(blackjacks)
        print "Win rate: " + str(win * 100 / hand) + "%"
        output = "Winnings: "
        if winnings >= 0:
            output += "$" + ("%.2f" % winnings)
        else:
            output += "-$" + ("%.2f" % -winnings)
        print output
        
    print "\nThanks for playing!"
    print "\n*******************************************"

###############################################################################
##### AUXILLIARY FUNCTIONS
###############################################################################

# main function for a single blackjack hand - called each round
def play_hand(verbose=True, soft=True, strategy="Manual"):
    print_verbose(verbose, "\n*******************************************")
    
    player = []                    # player's hand
    dealer = []                    # dealer's hand
    random.shuffle(DECK)           # shuffle the deck
    position = 4                   # current position in deck (after dealing)
    
    # deal cards and print hands
    player, dealer = deal_cards(DECK, player, dealer)
    if verbose:    
        current_state(player, dealer)

    #player's turn
    player_result, position = players_round(player, position, verbose, strategy)
    
    if player_result == -1:
        print_verbose(verbose, "BUST: dealer wins")
        return -1
    
    # dealer's turn    
    dealer_result = dealers_round(dealer, position, verbose, soft)
    
    if dealer_result == -1:
        print_verbose(verbose, "DEALER BUST: player wins")
        return 1
    elif dealer_result > player_result:
        output = "DEALER WINS: " + str(dealer_result)
        output += " beats " + str(player_result)
        print_verbose(verbose, output)
        return -1
    elif dealer_result == player_result:
        print_verbose(verbose, "DRAW: both players have " + str(dealer_result))
        return 0
    else:
        output = "PLAYER WINS: " + str(player_result)
        output += " beats " + str(dealer_result)
        print_verbose(verbose, output)
        if position == 4:
            return 2
        else:
            return 1        

# prints a welcome message with the game's rules
def welcome_message():
    message = """\nWelcome to Blackjack!
    Author: Will Moyle
    Last Modified: 20 Nov 2015
    
    The aim of the game is to beat the dealer's hand by getting a hand 
    with a score closer to 21 but not over. Aces are worth 1 or 11 points. 
    Tens, Jacks, Queens and Kings are worth 10 points."
    
    Good luck!"""
    
    print message

# deals the first hand    
def deal_cards(deck, player, dealer):
    player = [DECK[0], DECK[2]]
    dealer = [DECK[1], DECK[4]]
    return player, dealer
    
# prints the current hands after the cards have been dealt
def current_state(player, dealer):
    print "\nThe dealer's hand: " + display_hand(dealer, True)
    print "\nYour hand: " + display_hand(player)
    print "which is worth: " + display_scores(calculate_score(player))
    
# returns a string representing the cards in a given hand
def display_hand(hand, first_round=False):    
    hand_description = CARD_NAMES.get(hand[0])
    if first_round:
        hand_description += " and UNKNOWN"
    else: 
        for i, card in enumerate(hand):
            if i > 0:
                hand_description += ", " + CARD_NAMES.get(card)
    return hand_description            

# returns a string representing the points of the given hand
def display_scores(scores):
    score_description = str(scores[0])
    for i, score in enumerate(scores):
        if i > 0:
            score_description += " or " + str(score)
    return score_description

# calculates all possible scores of a given hand
def calculate_score(hand):
    base_score = 0
    number_aces = 0
    for card in hand:
        if card == 0:
            base_score += 1
            number_aces += 1
        elif card <= 9:
            base_score += card + 1
        else:
            base_score += 10
    scores = [base_score]
    for _ in range(number_aces):
        base_score += 10
        if base_score <= 21:
            scores.append(base_score)
    return scores

# handles the player's turn including his decisions        
def players_round(player, position, verbose=True, strategy="Manual"):
    player_scores = calculate_score(player)

    if 21 in player_scores:
        
        print_verbose(verbose, "BLACKJACK!")
        return 21, position
    
    while(True):
        action = player_sticks(player_scores, strategy)
        if not action:
            player += [DECK[position]]
            player_scores = calculate_score(player)            
            position += 1
            if verbose:            
                print "\nYour hand: " + display_hand(player)
                print "which is worth: " + display_scores(player_scores)
            if player_scores[0] > 21:
                return -1, position
            if 21 in player_scores:
                return 21, position
        else:
            if len(player_scores) > 1 and player_scores[1] <= 21:           
                return player_scores[1], position
            else:
                return player_scores[0], position

# returns true if the player decides to stick with hand 's'
def player_sticks(s, strategy="Manual"):
    if strategy == "Manual":
        while(True):
            action = raw_input("Do you wish to stick (S) or hit (H)? ")
            if action == 'H' or action == 'h':
                return False
            elif action == 'S' or action == 's':
                return True
            else:
                print "Invalid input"
    elif strategy == "Hard 16":
        return s[0] in range(16, 22)
    elif strategy == "Hard 17":
        return s[0] in range(17, 22)
    elif strategy == "Hard 18":
        return s[0] in range(18, 22)
    elif strategy == "Hard 19":
        return s[0] in range(19, 22)
    elif strategy == "Hard 20":
        return s[0] in range(20, 22)
    elif strategy == "Hard 21":
        return s[0] == 21
    elif strategy == "Soft 16":    
        return 16 in s or 17 in s or 18 in s or 19 in s or 20 in s or 21 in s
    elif strategy == "Soft 17":    
        return 17 in s or 18 in s or 19 in s or 20 in s or 21 in s
    elif strategy == "Soft 18":    
        return 18 in s or 19 in s or 20 in s or 21 in s
    elif strategy == "Soft 19":    
        return 19 in s or 20 in s or 21 in s
    elif strategy == "Soft 20":    
        return 20 in s or 21 in s
    elif strategy == "Soft 21":    
        return 21 in s
        
# handles the dealer's turn    
def dealers_round(dealer, position, verbose=True, soft=True):
    dealers_scores = calculate_score(dealer)
    
    if verbose:
        print "\nThe dealer's hand: " + display_hand(dealer)
        print "which is worth: " + display_scores(calculate_score(dealer))
    
    if 21 in dealers_scores:
        print_verbose(verbose, "Dealer has natural 21")
        return 21
        
    while(True):
        dealers_scores = calculate_score(dealer)
        if dealers_scores[0] > 21:
            return -1
        elif dealer_sticks(dealers_scores, soft):
            score = dealers_scores[0]
            for i in dealers_scores:
                if i <= 21:                
                    score = i
            print_verbose(verbose, "\nDealer sticks on " + str(score))
            return score
        else:
            dealer += [DECK[position]]
            position += 1
            output = "\nDealer hits\nThe dealer's hand: "+ display_hand(dealer)
            output += "\nwhich is worth: "
            output += display_scores(calculate_score(dealer))
            print_verbose(verbose, output)
                
            
# returns true if the score 's' results in the dealer sticking            
def dealer_sticks(s, soft=True):
    if soft:    
        return 17 in s or 18 in s or 19 in s or 20 in s or 21 in s
    else:
        return s[0] in range(17, 22)
        
# returns the number if the string input is an integer greater than 0, else -1
def natural_number(string):
    try:
        num = int(string)
        if num > 0:
            return num
        else:
            return -1
    except ValueError:
        return -1
        
# returns the number if the string input is a valid number greater than 0
def positive_number(string):
    try:
        num = float(string)
        if num > 0:
            return num
        else:
            return -1
    except ValueError:
        return -1
        
# prints the string only if verbose is true
def print_verbose(verbose, string):
    if verbose:
        print string

play_blackjack()
