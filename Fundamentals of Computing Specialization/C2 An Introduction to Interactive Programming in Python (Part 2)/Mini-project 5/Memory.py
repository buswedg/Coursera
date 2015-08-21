## An Introduction to Interactive Programming in Python (Part 2)
## Mini-project 5: Memory
## Memory.py

## Required packages:
## pygame - http://www.pygame.org/download.shtml
## SimpleGUICS2Pygame - https://simpleguics2pygame.readthedocs.org/

## Module was initially intended to be run with CodeSkulptor http://www.codeskulptor.org/#examples-memory_template.py
## In order to run on local Phython instance, call to import module 'simplegui' has been modified.

# Implementation of classic arcade game Pong

# import simplegui
import SimpleGUICS2Pygame.simpleguics2pygame as simplegui
import random

WIDTH = 800
HEIGHT = 100
FIELDS = 16
FIELD_WIDTH = 800 // 16
NUMBER_SPACES = 50
LINE_WIDTH = 2

# helper function to initialize globals
def new_game():
    global numbers, exposed, state, moves
    numbers = [i % 8 for i in range(16)]
    random.shuffle(numbers)
    exposed = [False for i in range(16)]
    state = 0
    moves = 0

# define event handlers
def mouseclick(pos):
    global exposed, state, last_exposed, last_last_exposed, moves
    field_number = pos[0] // FIELD_WIDTH

    if not exposed[field_number]: 
        if state == 0:
            exposed[field_number] = True    
            last_last_exposed = field_number
            state = 1
        elif state == 1:
            exposed[field_number] = True
            last_exposed = field_number
            state = 2
        elif state == 2:
            exposed[field_number] = True
            if numbers[last_last_exposed] == numbers[last_exposed]:
                pass
            else:
                exposed[last_last_exposed] = False
                exposed[last_exposed] = False
            last_last_exposed = field_number
            state = 1
            moves += 1
                        
# cards are logically 50x100 pixels in size    
def draw(canvas):
    global moves
    for i in range(0, FIELDS - 1):
        x = (i+1) * FIELD_WIDTH
        canvas.draw_line((x, 0), (x, HEIGHT), LINE_WIDTH, "White")
    field = 0
    offset = NUMBER_SPACES / 5
    for n in numbers:
        canvas.draw_text(str(n), (offset + field * NUMBER_SPACES, 65), 42, "White")
        field += 1
    field = 0
    for n in numbers:
        if not exposed[field]:
            canvas.draw_polygon([[field * FIELD_WIDTH, 0], [(field + 1) * FIELD_WIDTH, 0], [(field + 1) * FIELD_WIDTH, HEIGHT], [field * FIELD_WIDTH, HEIGHT]], LINE_WIDTH, "White", "Green")
        field += 1
    l.set_text("Moves = " + str(moves))
    
# create frame and add a button and labels
frame = simplegui.create_frame("Memory", WIDTH, HEIGHT)
frame.add_button("Restart", new_game)
l = frame.add_label("Moves = 0")

# initialize global variables
new_game()

# register event handlers
frame.set_mouseclick_handler(mouseclick)
frame.set_draw_handler(draw)

# get things rolling
frame.start()


# Always remember to review the grading rubric