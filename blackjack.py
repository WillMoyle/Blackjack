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

###############################################################################
##### MAIN FUNCTION
###############################################################################

def play_blackjack():
    welcome_message()
    
    keep_playing = True
    win = 0
    loss = 0
    draw = 0
    hand = 0
    
    while(keep_playing):
        result = play_hand()
        hand += 1
        if result == -1:
            loss += 1
        elif result == 0:
            draw += 1
        else:
            win += 1
        print "\nAfter round " + str(hand) + " the results are:"
        print "Wins: " + str(win)
        print "Draws: " + str(draw)
        print "Losses: " + str(loss)
        again = raw_input("Do you wish to play another round? (Y/N)")
        if again == 'Y' or again == 'y':
            continue
        else:
            keep_playing = False
            
    print "\nThanks for playing!"


###############################################################################
##### AUXILLIARY FUNCTIONS
###############################################################################

def play_hand():
    
    #define main variables
    
    player = []                         # player's hand
    dealer = []                         # dealer's hand
    
    random.shuffle(DECK)                # shuffle the deck
        
    # deal cards and print hands
    player, dealer = deal_cards(DECK, player, dealer)
    current_state(player, dealer)
    
    position = 4                        # current position in deck

    player_result, position = players_round(player, position)
    
    if player_result == -1:
        print "BUST: dealer wins"
        return -1
        
    dealer_result = dealers_round(dealer, position)
    
    if dealer_result == -1:
        print "DEALER BUST: player wins"
        return 1
    elif dealer_result > player_result:
        print "DEALER WINS: " + str(dealer_result) + " beats " + str(player_result)
        return -1
    elif dealer_result == player_result:
        print "DRAW: both players have " + str(dealer_result)
        return 0
    else:
        print "PLAYER WINS: " + str(player_result) + " beats " + str(dealer_result)
        return 1        
    

    return 0

def welcome_message():
    message = """\nWelcome to Blackjack!
    Author: Will Moyle
    Last Modified: 20 Nov 2015
    
    The aim of the game is to beat the dealer's hand by getting a hand 
    with a score closer to 21 but not over. Aces are worth 1 or 11 points. 
    Tens, Jacks, Queens and Kings are worth 10 points. Dealer must draw on
    16 and stand on all soft 17's."
    
    Good luck!"""
    
    print message
    
def deal_cards(deck, player, dealer):
    player = [DECK[0], DECK[2]]
    dealer = [DECK[1], DECK[4]]
    print "\nThe cards have been delt" 
    return player, dealer
    
def current_state(player, dealer, first_round=True):
    print "\nThe dealer's hand: " + display_hand(dealer, first_round)
    if not first_round:    
        print "which is worth: " + display_scores(calculate_score(dealer))
    
    print "\nYour hand: " + display_hand(player)
    print "which is worth: " + display_scores(calculate_score(player))
    
def display_hand(hand, first_round=False):    
    hand_description = CARD_NAMES.get(hand[0])
    if first_round:
        hand_description += " and UNKNOWN"
    else: 
        for i, card in enumerate(hand):
            if i > 0:
                hand_description += ", " + CARD_NAMES.get(card)
    return hand_description            

def display_scores(scores):
    score_description = str(scores[0])
    for i, score in enumerate(scores):
        if i > 0:
            score_description += " or " + str(score)
    return score_description
    
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
        
def players_round(player, position):
    player_scores = calculate_score(player)

    if 21 in player_scores:
        print "BLACKJACK!"
        return 21, position
    
    while(True):
        action = raw_input("Do you wish to stick (S) or hit (H)?")
        if action == 'H' or action == 'h':
            player += [DECK[position]]
            player_scores = calculate_score(player)            
            position += 1
            print "\nYour hand: " + display_hand(player)
            print "which is worth: " + display_scores(player_scores)
            if player_scores[0] > 21:
                return -1, position
            if 21 in player_scores:
                return 21, position
        elif action == 'S' or action == 's':
            if len(player_scores) > 1 and player_scores[1] <= 21:           
                return player_scores[1], position
            else:
                return player_scores[0], position
        else:
            print "Invalid input"
    
def dealers_round(dealer, position):
    dealers_scores = calculate_score(dealer)
    
    print "\nThe dealer's hand: " + display_hand(dealer)
    print "which is worth: " + display_scores(calculate_score(dealer))
    
    if 21 in dealers_scores:
        print "Dealer has natural 21"
        return 21
        
    while(True):
        dealers_scores = calculate_score(dealer)
        if dealers_scores[0] > 21:
            return -1
        elif dealer_sticks(dealers_scores):
            score = dealers_scores[0]
            for i in dealers_scores:
                if i <= 21:                
                    score = i
            print "\nDealer sticks on " + str(score)
            return score
        else:
            print "\nDealer hits"           
            dealer += [DECK[position]]
            dealer_scores = calculate_score(dealer)
            position += 1
            print "The dealer's hand: " + display_hand(dealer)
            print "which is worth: " + display_scores(calculate_score(dealer))
            
            
def dealer_sticks(s):
    return 17 in s or 18 in s or 19 in s or 20 in s or 21 in s
        
play_blackjack()
