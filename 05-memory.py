# implementation of card game - Memory

import simpleguitk as simplegui
import random

# define globals
cardList = []
firstCard = []
numExposed = 0
moves = 0

# helper function to initialize globals
def init():
    global cardList, numExposed, moves
    cardList = []
    numExposed = 0
    moves = 0
    l.set_text("Moves = 0")
    for i in range(16):
        cardList.append([i//2, "Grey", "Grey"])
        random.shuffle(cardList)
    
# define event handlers
def mouseclick(pos):
    global numExposed, firstCard, moves
    
    if numExposed == 2:
        for i in range(len(cardList)):
            if cardList[i][2] != "White":
                cardList[i][1] = "Grey"
                cardList[i][2] = "Grey"
                numExposed = 0
    
    for i in range(len(cardList)):
        if pos[0] > (i*50) and pos[0] < (i*50+50) and (cardList[i][1] == "Grey"):
            cardList[i][1] = "Green"
            cardList[i][2] = "Yellow"
            numExposed += 1
            
            # if one card has been exposed, store its value
            if numExposed % 2 == 1:
                firstCard = cardList[i]
            elif numExposed % 2 == 0:
                # if two cards have been exposed and they match...
                if cardList[i][0] == firstCard[0]:
                    cardList[i][2] = "White"
                    firstCard[2] = "White"
                    numExposed = 0
                moves +=1
                l.set_text("Moves = " + str(moves))
                        
# cards are logically 50x100 pixels in size    
def draw(canvas):    
    # draw the cards
    for i in range(len(cardList)):
        canvas.draw_polygon([(i*50,0),
                         (i*50+50,0),
                         (i*50+50,100),
                         (i*50,100)], 6, "Green", cardList[i][1])
    
    # draw the numbers
    for i in range(len(cardList)):
        canvas.draw_text(str(cardList[i][0]), (50*i+10,70), 42, cardList[i][2]) 

# create frame and add a button and labels
frame = simplegui.create_frame("Memory", 800, 100)
frame.add_button("Restart", init)
l=frame.add_label("Moves = 0")

# initialize global variables
init()

# register event handlers
frame.set_mouseclick_handler(mouseclick)
frame.set_draw_handler(draw)

# Start the frame
frame.start()

# Always remember to review the grading rubric
