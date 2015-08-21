## An Introduction to Interactive Programming in Python (Part 1)
## Mini-project 2: Guess the Number Game
## Guess_the_Number.py

## Required packages:
## pygame - http://www.pygame.org/download.shtml
## SimpleGUICS2Pygame - https://simpleguics2pygame.readthedocs.org/

## Module was initially intended to be run with CodeSkulptor http://www.codeskulptor.org/#examples-guess_the_number_template.py
## In order to run on local Phython instance, call to import module 'simplegui' has been modified.

# template for "Guess the number" mini-project
# input will come from buttons and an input field
# all output for the game will be printed in the console

## import simplegui
import SimpleGUICS2Pygame.simpleguics2pygame as simplegui
import random
import math


# initialize global variables used in your code
secret_number = None
num_range = 100
remaining_guesses = None


# helper function to start and restart the game
def new_game():
    # initialize global variables used in your code
    global num_range
    global secret_number
    secret_number = random.randrange(num_range)

    global remaining_guesses
    remaining_guesses = int(math.ceil(math.log(num_range + 1, 2)))

    print ("New game. Range is from 0 to", num_range)
    print ("Number of remaining guesses is", remaining_guesses)
    print


# define event handlers for control panel
def range100():
    # button that changes the range to [0,100) and starts a new game 
    global num_range
    num_range = 100
    new_game()

    
def range1000():
    # button that changes the range to [0,1000) and starts a new game
    global num_range
    num_range = 1000
    new_game()

    
def input_guess(guess):
    # main game logic goes here	
    global secret_number
    global remaining_guesses

    completed_game = False

    guess = int(guess)
    print ("Guess was", guess)

    remaining_guesses -= 1
    print ("Number of remaining guesses is", remaining_guesses)

    if guess == secret_number:
        print ("Correct!")
        print
        completed_game = True
    elif remaining_guesses <= 0:
        print ("You ran out of guesses. The number was", secret_number)
        print
        completed_game = True
    elif guess > secret_number:
        print ("Lower!")
        print
    else:
        print ("Higher!")
        print

    if completed_game:
        new_game()


# create frame
frame = simplegui.create_frame("Guess the Number", 300, 300)

# register event handlers for control elements
frame.add_input("Guess", input_guess, 100)
frame.add_button("Range 0 - 100", range100, 100)
frame.add_button("Range 0 - 1000", range1000, 100)

# call new_game
new_game()
frame.start()



###################################################
# Start our test #1 - assume global variable secret_number
# is the the "secret number" - change name if necessary

#secret_number = 74	
#input_guess("50")
#input_guess("75")
#input_guess("62")
#input_guess("68")
#input_guess("71")
#input_guess("73")
#input_guess("74")

###################################################
# Output from test #1
#New game. Range is from 0 to 100
#Number of remaining guesses is 7
#
#Guess was 50
#Number of remaining guesses is 6
#Higher!
#
#Guess was 75
#Number of remaining guesses is 5
#Lower!
#
#Guess was 62
#Number of remaining guesses is 4
#Higher!
#
#Guess was 68
#Number of remaining guesses is 3
#Higher!
#
#Guess was 71
#Number of remaining guesses is 2
#Higher!
#
#Guess was 73
#Number of remaining guesses is 1
#Higher!
#
#Guess was 74
#Number of remaining guesses is 0
#Correct!
#
#New game. Range is from 0 to 100
#Number of remaining guesses is 7

###################################################
# Start our test #2 - assume global variable secret_number
# is the the "secret number" - change name if necessary

#range1000()
#secret_number = 375	
#input_guess("500")
#input_guess("250")
#input_guess("375")

###################################################
# Output from test #2
#New game. Range is from 0 to 100
#Number of remaining guesses is 7
#
#New game. Range is from 0 to 1000
#Number of remaining guesses is 10
#
#Guess was 500
#Number of remaining guesses is 9
#Lower!
#
#Guess was 250
#Number of remaining guesses is 8
#Higher!
#
#Guess was 375
#Number of remaining guesses is 7
#Correct!
#
#New game. Range is from 0 to 1000
#Number of remaining guesses is 10



###################################################
# Start our test #3 - assume global variable secret_number
# is the the "secret number" - change name if necessary

#secret_number = 28	
#input_guess("50")
#input_guess("50")
#input_guess("50")
#input_guess("50")
#input_guess("50")
#input_guess("50")
#input_guess("50")

###################################################
# Output from test #3
#New game. Range is from 0 to 100
#Number of remaining guesses is 7
#
#Guess was 50
#Number of remaining guesses is 6
#Lower!
#
#Guess was 50
#Number of remaining guesses is 5
#Lower!
#
#Guess was 50
#Number of remaining guesses is 4
#Lower!
#
#Guess was 50
#Number of remaining guesses is 3
#Lower!
#
#Guess was 50
#Number of remaining guesses is 2
#Lower!
#
#Guess was 50
#Number of remaining guesses is 1
#Lower!
#
#Guess was 50
#Number of remaining guesses is 0
#You ran out of guesses.  The number was 28
#
#New game. Range is from 0 to 100
#Number of remaining guesses is 7
