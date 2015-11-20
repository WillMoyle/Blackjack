#Blackjack simulator and statistical analysis tool

Author: Will Moyle
Last Modified 20 Nov 2015

A command line tool, written in Python, that allows the user to either:
- play a game of blackjack against the computer, choosing when to stick or hit manually
- choose a strategy for the player and automatically run a given number of games and analyse the results

The user is asked:
- What is their strategy. Can be either "Manual", "Soft 16-18" or "Hard 16-18" (e.g. input "Soft 16")
- How much the user wants to bet each hand
- What the multiplier for blackjack wins is (e.g. 1.5)
- Whether the dealer should stand on a soft 17 or hard 17 (varies by casino)
- If the user's strategy is not "Manual" then the user inputs how many hands they wish to play and whether they want to see details of each hand

At the end, the program outputs the total number of wins, losses, draws and blackjack wins, along with the win rate (as a percentage) and the total monetary winnings or losses.

For a detailed set of rules for blackjack (used for reference in developing this program), visit http://www.pagat.com/banking/blackjack.html
