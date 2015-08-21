## An Introduction to Interactive Programming in Python (Part 1)
## Mini-project 4: Pong
## Pong.py

## Required packages:
## pygame - http://www.pygame.org/download.shtml
## SimpleGUICS2Pygame - https://simpleguics2pygame.readthedocs.org/

## Module was initially intended to be run with CodeSkulptor http://www.codeskulptor.org/#examples-pong_template.py
## In order to run on local Phython instance, call to import module 'simplegui' has been modified.

# Implementation of classic arcade game Pong

# import simplegui
import SimpleGUICS2Pygame.simpleguics2pygame as simplegui
import random

# initialize globals - pos and vel encode vertical info for paddles
WIDTH = 600
HEIGHT = 400       
BALL_RADIUS = 20
PAD_WIDTH = 8
PAD_HEIGHT = 80
HALF_PAD_WIDTH = PAD_WIDTH / 2
HALF_PAD_HEIGHT = PAD_HEIGHT / 2
LEFT = False
RIGHT = True

# new game variables
score1 = 0
score2 = 0
paddle1_pos = HEIGHT / 2
paddle2_pos = HEIGHT / 2
paddle1_vel = 0
paddle2_vel = 0
ball_pos = [WIDTH / 2 , HEIGHT / 2]
ball_vel = [random.randrange(60, 180) / 60, random.randrange(120, 240) / 60]


# initialize ball_pos and ball_vel for new bal in middle of table
# if direction is RIGHT, the ball's velocity is upper right, else upper left
def spawn_ball(DIRECTION):
    global ball_pos, ball_vel # these are vectors stored as lists
    
    ball_pos = [WIDTH / 2 , HEIGHT / 2]
    ball_vel[1] = -random.randrange(60, 180) / 60
    
    if DIRECTION == RIGHT:
        ball_vel[0] = random.randrange(120, 240) / 60
    else:
        ball_vel[0] = -random.randrange(120, 240) / 60
    pass


# define event handlers
def new_game():
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel  # these are numbers
    global score1, score2  # these are ints
    
    # new game variables
    score1 = 0
    score2 = 0
    paddle1_pos = HEIGHT / 2
    paddle2_pos = HEIGHT / 2
    paddle1_vel = 0
    paddle2_vel = 0
    ball_pos = [WIDTH / 2 , HEIGHT / 2]
    
    RIGHT = True
    spawn_ball(RIGHT)


def draw(canvas):
    global score1, score2, paddle1_pos, paddle2_pos, ball_pos, ball_vel

    # draw mid line and gutters
    canvas.draw_line([WIDTH / 2, 0],[WIDTH / 2, HEIGHT], 1, "White")
    canvas.draw_line([PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1, "White")
    canvas.draw_line([WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 1, "White")

    # print instructions
    canvas.draw_text("'w' to move up. 's' to move down.", (15, 395), 10, "White", "monospace")
    canvas.draw_text("'up' to move up. 'down' to move down.", (WIDTH / 2 + 10, 395), 10, "White", "monospace")
    
    # update ball
    ball_pos[0] += ball_vel[0]
    ball_pos[1] += ball_vel[1]    
    
    if ball_pos[1] < BALL_RADIUS:
        ball_vel[1] = -ball_vel[1]
    if ball_pos[1] > HEIGHT - BALL_RADIUS:
        ball_vel[1] = -ball_vel[1]
   
    if ball_pos[0] - BALL_RADIUS < PAD_WIDTH:
        if ball_pos[1] < paddle2_pos - PAD_HEIGHT or ball_pos[1] > paddle2_pos + HALF_PAD_HEIGHT:
            spawn_ball(RIGHT)
            score2 += 1    
        else:
            ball_vel[0] = -ball_vel[0] * 1.1
            
    if  ball_pos[0] + BALL_RADIUS > WIDTH - PAD_WIDTH:
        if ball_pos[1] < (paddle1_pos - PAD_HEIGHT) or ball_pos[1] > (paddle1_pos + HALF_PAD_HEIGHT):
            spawn_ball(LEFT)
            score1 += 1
        else:
            ball_vel[0] = -ball_vel[0] * 1.1   
           
    # draw ball  
    ball = canvas.draw_circle(ball_pos, BALL_RADIUS, 2, "White", "White")

    # update paddle's vertical position, keep paddle on the screen
    paddle1_pos += paddle1_vel
    paddle2_pos += paddle2_vel
     
    # draw paddles
    paddle1 = canvas.draw_line([HALF_PAD_WIDTH, paddle2_pos + HALF_PAD_HEIGHT], [HALF_PAD_WIDTH,paddle2_pos - HALF_PAD_HEIGHT],8, "White")
    paddle2 = canvas.draw_line([WIDTH - HALF_PAD_WIDTH,paddle1_pos + HALF_PAD_HEIGHT], [WIDTH - HALF_PAD_WIDTH,paddle1_pos - HALF_PAD_HEIGHT],8, "White")

    if paddle1_pos <= HALF_PAD_HEIGHT:
        paddle1_pos = HALF_PAD_HEIGHT
    if paddle2_pos <= HALF_PAD_HEIGHT:
        paddle2_pos = HALF_PAD_HEIGHT
       
    if paddle1_pos >= HEIGHT - HALF_PAD_HEIGHT:
        paddle1_pos = HEIGHT - HALF_PAD_HEIGHT
    if paddle2_pos >= HEIGHT - HALF_PAD_HEIGHT:
        paddle2_pos = HEIGHT - HALF_PAD_HEIGHT

    # draw scores
    canvas.draw_text(str(score1), (120, 200), 80, "grey")
    canvas.draw_text(str(score2), (420, 200), 80, "grey")  


def keydown(key):
    global paddle1_vel, paddle2_vel
    
    if key == simplegui.KEY_MAP['up']:
        paddle1_vel = -5
    elif key == simplegui.KEY_MAP['down']:
        paddle1_vel = 5
    elif key == simplegui.KEY_MAP['w']:
        paddle2_vel = -5
    elif key == simplegui.KEY_MAP['s']:
        paddle2_vel = 5
   

def keyup(key):
    global paddle1_vel, paddle2_vel
    
    if key == simplegui.KEY_MAP['up']:
        paddle1_vel = 0
    elif key == simplegui.KEY_MAP['down']:
        paddle1_vel = 0
    elif key == simplegui.KEY_MAP['w']:
        paddle2_vel = 0
    elif key == simplegui.KEY_MAP['s']:
        paddle2_vel = 0
                               

# create frame
frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
frame.add_button("Reset", new_game, 150)


# start frame
new_game()
frame.start()