## An Introduction to Interactive Programming in Python (Part 1)
## Mini-project 1: Rock-paper-scissors-lizard-Spock
## Rock-Paper-Scissors-Lizard-Spock.py

## Module was initially intended to be run with CodeSkulptor http://www.codeskulptor.org/#examples-rpsls_template.py


# The key idea of this program is to equate the strings
# "rock", "paper", "scissors", "lizard", "Spock" to numbers
# as follows:
#
# 0 - rock
# 1 - Spock
# 2 - paper
# 3 - lizard
# 4 - scissors

import random

# helper functions

def number_to_name(number):
    if number == 0:
        return "rock"
    elif number == 1:
        return "Spock"
    elif number == 2:
        return "paper"
    elif number == 3:
        return "lizard"
    elif number == 4:
        return "scissors"
    else:
        return "Invalid number"
    
def name_to_number(name):
    if name == "rock":
        return 0
    elif name == "Spock":
        return 1
    elif name == "paper":
        return 2
    elif name == "lizard":
        return 3
    elif name == "scissors":
        return 4
    else:
        return "Invalid name"

def rpsls(name): 
    player_number = name_to_number(name)

    comp_number = random.randrange(0, 5)
    
    difference = (player_number - comp_number) % 5
    
    if difference == 0:
        result = "Tie game"
    elif difference == 1 or difference == 2:
        result = "Player wins!"
    else:
        result = "Computer wins!"
    
    comp_name = number_to_name (comp_number)
    
    print ("Player chooses"), name
    print ("Computer chooses"), comp_name
    print (result)

    if name != "scissors":
        print
    
# test code
rpsls("rock")
rpsls("Spock")
rpsls("paper")
rpsls("lizard")
rpsls("scissors")
