# Implementation of classic arcade game Pong

import simpleguitk as simplegui
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

# initialize ball_pos and ball_vel for new ball in middle of table
ball_pos = [WIDTH / 2, HEIGHT / 2]
ball_vel = [0, 0]

# if direction is RIGHT, the ball's velocity is upper right, else upper left
def spawn_ball(direction):
    global ball_pos, ball_vel # these are vectors stored as lists
    ball_pos = [WIDTH / 2, HEIGHT / 2]
    ball_vel[0] = random.randrange(120, 240)
    ball_vel[1] = -random.randrange(60, 180)
    if direction == LEFT:
        ball_vel[0] *= -1
    ball_pos += ball_vel


# define event handlers
def new_game():
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel  # these are numbers
    global score1, score2  # these are ints
    paddle1_pos = HEIGHT / 2 - HALF_PAD_HEIGHT
    paddle2_pos = HEIGHT / 2 - HALF_PAD_HEIGHT
    paddle1_vel = 0
    paddle2_vel = 0
    score1 = 0
    score2 = 0
    spawn_ball(LEFT)

def draw(canvas):
    global score1, score2, paddle1_pos, paddle2_pos, ball_pos, ball_vel

    # draw mid line and gutters
    canvas.draw_line([WIDTH / 2, 0],[WIDTH / 2, HEIGHT], 2, "White") # Center Line
    canvas.draw_line([PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 2, "White") # Left Gutter
    canvas.draw_line([WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 2, "White") # Right Gutter
    
    # update ball
    
    # Reflecting the ball from Top & Bottom Gutters
    if ball_pos[1] <= BALL_RADIUS or ball_pos[1] >= HEIGHT - BALL_RADIUS:
        ball_vel[1] *= -1
    ball_pos[1] += ball_vel[1] * 0.03
    
    # Reflecting the ball from Left & Right Paddles
    if ball_pos[0] < (PAD_WIDTH + BALL_RADIUS):
        if ball_pos[1] >= paddle1_pos and ball_pos[1] <= paddle1_pos + PAD_HEIGHT:
            ball_vel[0] *= -1.1
        else:
            spawn_ball(RIGHT)
            score2 += 1

    if ball_pos[0] > WIDTH - (PAD_WIDTH + BALL_RADIUS):
        if ball_pos[1] >= paddle2_pos and ball_pos[1] <= paddle2_pos + PAD_HEIGHT:
            ball_vel[0] *= -1.1
        else:
            spawn_ball(LEFT)
            score1 += 1
            
    ball_pos[0] += ball_vel[0] * 0.03
    
    # draw ball
    canvas.draw_circle(ball_pos, BALL_RADIUS, 2, "Red", "White")
    
    # update paddle's vertical position, keep paddle on the screen

    paddle1_pos += paddle1_vel # Left Paddle
    
    if paddle1_pos < 0:
        paddle1_pos = 0
    if paddle1_pos > (HEIGHT - PAD_HEIGHT):
        paddle1_pos = HEIGHT - PAD_HEIGHT

    paddle2_pos += paddle2_vel # Right Paddle
    
    if paddle2_pos < 0:
        paddle2_pos = 0
    if paddle2_pos > (HEIGHT - PAD_HEIGHT):
        paddle2_pos = HEIGHT - PAD_HEIGHT

    # draw paddles
    canvas.draw_line([HALF_PAD_WIDTH, paddle1_pos], [HALF_PAD_WIDTH, paddle1_pos + PAD_HEIGHT], PAD_WIDTH, "Yellow")
    canvas.draw_line([WIDTH - HALF_PAD_WIDTH, paddle2_pos], [WIDTH - HALF_PAD_WIDTH, paddle2_pos + PAD_HEIGHT], PAD_WIDTH, "Blue")

    # draw scores
    canvas.draw_text(score1, (WIDTH / 2 - 50, 40), 20, 'Yellow')
    canvas.draw_text(score2, (WIDTH / 2 + 10, 40), 20, 'Blue')

def keydown(key):
    global paddle1_vel, paddle2_vel, paddle1_pos, paddle2_pos

    if key == simplegui.KEY_MAP["w"]:
        paddle1_vel = -8
    elif key == simplegui.KEY_MAP["s"]:
        paddle1_vel = 8

    if key == simplegui.KEY_MAP["up"]:
        paddle2_vel = -8
    elif key == simplegui.KEY_MAP["down"]:
        paddle2_vel = 8

def keyup(key):
    global paddle1_vel, paddle2_vel
    paddle1_vel = 0
    paddle2_vel = 0

# create frame
frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)
frame.set_canvas_background('Green')
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
frame.add_button('RESTART', new_game, 100)

# start frame
new_game()
frame.start()
