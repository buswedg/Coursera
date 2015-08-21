## An Introduction to Interactive Programming in Python (Part 1)
## Mini-project 3: Stopwatch: The Game
## Stopwatch_Game.py

## Required packages:
## pygame - http://www.pygame.org/download.shtml
## SimpleGUICS2Pygame - https://simpleguics2pygame.readthedocs.org/

## Module was initially intended to be run with CodeSkulptor http://www.codeskulptor.org/#examples-stopwatch_template.py
## In order to run on local Phython instance, call to import module 'simplegui' has been modified.

# template for "Stopwatch: The Game"

## import simplegui
import SimpleGUICS2Pygame.simpleguics2pygame as simplegui


# define global variables
counter = 0
t = 0
tries = 0
wins = 0
last_stop = 0


# define helper function format that converts time
# in tenths of seconds into formatted string A:BC.D
def format(t):
    global counter
    a = counter // 600
    b = ((counter // 100) % 6)
    c = (counter // 10) % 10
    d = counter % 10
    return str(a) + ":" + str(b) + str(c) + "." + str(d)


# define event handlers for buttons; "Start", "Stop", "Reset"
def start():
    timer.start()
    
def stop():
    global tries
    global wins
    global last_stop
    timer.stop()
    if counter != last_stop:
        tries += 1
        last_stop = counter
        if counter%10 == 0:
                wins += 1
    update_score() 
    
def reset():
    global counter
    global tries
    global wins
    global last_stop
    timer.stop()
    counter = 0
    wins = 0
    tries = 0
    last_stop = 0


# define event handler for timer with 0.1 sec interval
def tick():
    global counter
    counter += 1
    return counter

	
# define draw handler
def draw(canvas):
    canvas.draw_text(format(t), (90, 160), 40, "Orange")
    canvas.draw_text(update_score(), (0, 25), 25, "White")

	
# update score
def update_score():
    global tries
    global wins
    return str(wins) + "/" + str(tries)


# create frame
frame = simplegui.create_frame("Stopwatch: The The Game", 300, 300)


# register event handlers
timer = simplegui.create_timer(100, tick)
frame.set_draw_handler(draw)
button1 = frame.add_button("Start", start, 50)
button2 = frame.add_button("Stop", stop, 50)
button3 = frame.add_button("Reset", reset, 50)


# start frame
frame.start()