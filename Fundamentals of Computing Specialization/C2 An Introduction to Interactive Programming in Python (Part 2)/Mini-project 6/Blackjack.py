## An Introduction to Interactive Programming in Python (Part 2)
## Mini-project 6: Blackjack
## Blackjack.py

## Required packages:
## pygame - http://www.pygame.org/download.shtml
## SimpleGUICS2Pygame - https://simpleguics2pygame.readthedocs.org/

## Module was initially intended to be run with CodeSkulptor http://www.codeskulptor.org/#examples-blackjack_template.py
## In order to run on local Phython instance, call to import module 'simplegui' has been modified.

# Mini-project #6 - Blackjack

# import simplegui
import SimpleGUICS2Pygame.simpleguics2pygame as simplegui
import random

# load card sprite - 936x384 - source: jfitz.com
CARD_SIZE = (72, 96)
CARD_CENTER = (36, 48)
card_images = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/cards_jfitz.png")

CARD_BACK_SIZE = (72, 96)
CARD_BACK_CENTER = (36, 48)
card_back = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/card_jfitz_back.png")    

# initialize some useful global variables
in_play = False
outcome = ""
score = 0

# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}


# define card class
class Card:
    def __init__(self, suit, rank):
        self.expose = 1
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
        else:
            self.suit = None
            self.rank = None
            print ("Invalid card: ", suit, rank)

    def __str__(self):
        return self.suit + self.rank

    def set_expose(self,expose):
        self.expose = expose
        
    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

    def draw(self, canvas, pos):
        if self.expose:
            card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank), 
                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
            canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)
        else:
            card_loc = (CARD_CENTER[0]+CARD_SIZE[0],CARD_CENTER[1])
            canvas.draw_image(card_back, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)
          
# define hand class
class Hand:
    def __init__(self):
        self.list = []  # create Hand object

    def __str__(self):
        str = ""
        for card in self.list:
            str += card.__str__ + " "
        return str  # return a string representation of a hand

    def add_card(self, card):
        self.list.append(card)	# add a card object to a hand
        
    def set_expose(self):
        self.list[0].set_expose(1)

    def get_value(self):
        # count aces as 1, if the hand has an ace, then add 10 to hand value if it doesn't bust
        sum = 0
        countace = 0
        for card in self.list:
            sum += VALUES[card.get_rank()]
            if card.get_rank() == 'A':
                countace += 1
        if countace == 1:
            if sum + 10 <= 21:
                sum += 10
        return sum  # compute the value of the hand, see Blackjack video
   
    def draw(self, canvas, pos):
         # draw a hand on the canvas, use the draw method for cards
        i = 0
        for card in self.list:
            card.draw(canvas, (pos[0] + i * (CARD_SIZE[0] + 10),pos[1]))
            i += 1
 
        
# define deck class 
class Deck:
    def __init__(self):
        # create a Deck object
        self.list = []
        for suit in SUITS:
            for rank in RANKS:
                card=Card(suit, rank)
                self.list.append(card)

    def shuffle(self):
        # shuffle the deck 
        random.shuffle(self.list)

    def deal_card(self):
        card = self.list.pop()
        return card
    
    def __str__(self):
        str = ""
        for card in self.list:
            str += card.__str__ + " "
        return str 


#define event handlers for buttons
def deal():
    global outcome, in_play, deck, player,dealer, in_play,score
    if in_play:
        score -= 1
    deck = Deck() 
    deck.shuffle()
    card1 = deck.deal_card()
    card1.set_expose(0)
    card2 = deck.deal_card()
    dealer = Hand()
    dealer.add_card(card1)
    dealer.add_card(card2)
    card1 = deck.deal_card()
    card2 = deck.deal_card()
    player = Hand()
    player.add_card(card1)
    player.add_card(card2)
    in_play = True

def hit():
    global score, in_play
    # if the hand is in play, hit the player
    if in_play:
        if player.get_value() <= 21:
            card1 = deck.deal_card()
            player.add_card(card1)  
        if player.get_value() > 21:
            print ("You have busted")
    # if busted, assign a message to outcome, update in_play and score
            score -= 1
            in_play = False
            dealer.set_expose()
            
def stand():
    global score, in_play
    # if hand is in play, repeatedly hit dealer until his hand has value 17 or more
    if in_play:
        while (dealer.get_value() <= 17):
            card1 = deck.deal_card()
            dealer.add_card(card1)
     # assign a message to outcome, update in_play and score 
        if dealer.get_value() > 21:
            print ("Dealer busted.")
            score += 1
            dealer.set_expose()
            in_play = False
        elif dealer.get_value() < player.get_value():
            print ("You won.")
            score += 1
            dealer.set_expose()
            in_play = False
        else:
            print ("You lost.")
            score -= 1
            dealer.set_expose()
            in_play = False

# draw handler    
def draw(canvas):
    # test to make sure that card.draw works, replace with your code below
    canvas.draw_text("Blackjack", [200, 80], 36, "Turquoise")
    canvas.draw_text("score: " + str(score), [385, 80], 30, "Black")
    canvas.draw_text("Dealer", [100, 120], 30, "Black")
    canvas.draw_text("Player", [100, 320], 30, "Black")
    if in_play:
        canvas.draw_text("Hit or Stand?", [200, 320], 30, "Black")
    else:
        canvas.draw_text("New Deal?", [200, 320], 30, "Black")
    player.draw(canvas, [100, 370])
    dealer.draw(canvas, [100, 170])


# initialization frame
frame = simplegui.create_frame("Blackjack", 600, 600)
frame.set_canvas_background("Green")

#create buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
frame.set_draw_handler(draw)


# get things rolling
deal()
frame.start()


# remember to review the gradic rubric
