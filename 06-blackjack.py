# Codeskulptor URL: http://www.codeskulptor.org/#user31_mr7wX4zLpr0iVtj.py

# Mini-project #6 - Blackjack

import simplegui
import random

# load card sprite - 949x392 - source: jfitz.com
CARD_SIZE = (73, 98)
CARD_CENTER = (36.5, 49)
card_images = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/cards.jfitz.png")

CARD_BACK_SIZE = (71, 96)
CARD_BACK_CENTER = (35.5, 48)
card_back = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/card_back.png")    

# initialize some useful global variables
in_play = False
outcome = ""
current = ""
score = 0
dealer = []
player = []
deck = []

# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}


# define card class
class Card:
    def __init__(self, suit, rank):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
        else:
            self.suit = None
            self.rank = None
            print "Invalid card: ", suit, rank

    def __str__(self):
        return self.suit + self.rank

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

    def draw(self, canvas, x, y, faceDown):
        card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank), 
                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
        canvas.draw_image(card_images, card_loc, CARD_SIZE, [x + CARD_CENTER[0], y + CARD_CENTER[1]], CARD_SIZE)
        if faceDown == True:
            card_loc = (CARD_BACK_CENTER[0], CARD_BACK_CENTER[1])
            canvas.draw_image(card_back, card_loc, CARD_BACK_SIZE, [x + CARD_BACK_CENTER[0], y + CARD_BACK_CENTER[1]], CARD_SIZE)
            
# define hand class
class Hand:
    def __init__(self):
        self.hand = []

    def __str__(self):
        return ','.join([card.get_suit()+card.get_rank() for card in self.hand])
    
    def add_card(self, card):
        self.hand.append(card)

    # count aces as 1, if the hand has an ace, then add 10 to hand value if it doesn't bust
    def get_value(self):
        value = 0
        ace = False
        for card in self.hand:
            value += VALUES[card.get_rank()]

        if self.count_aces() == 0: # No Aces
            return value
        else: # There is at least one Ace            
            if value + 10 > 21: # don't count that one ace as 11 if doing so would cause a bust
                return value
            else:
                return value + 10
    
    def hit(self, deck):
        self.add_card(deck.deal_card())

    def busted(self):
        global busted
        sum = self.get_value()
        if sum > 21:
            return True
            
    def draw(self, canvas, y):
        for card in self.hand:
            card.draw(canvas, 50+80*self.hand.index(card), y, False)
 
    def count_aces(self):
        aces = 0
        for card in self.hand:
            if card.get_rank() == 'A':
                aces += 1
        return aces

# define deck class
class Deck:
    def __init__(self):
        self.deck = []
        for s in SUITS:
            for r in RANKS:
                self.deck.append(Card(s, r))
        self.shuffle()

    # add cards back to deck and shuffle
    def shuffle(self):
        random.shuffle(self.deck)

    def deal_card(self):
        return self.deck.pop()


#define event handlers for buttons
def deal():
    global outcome, current, in_play, dealer, player, deck, score
    if in_play:
        score -= 1
    deck = Deck()
    dealer = Hand()
    player = Hand()
    outcome = ""
    current = "Hit or Stand ?"
    in_play = True
    dealer.hit(deck)
    player.hit(deck)
    dealer.hit(deck)
    player.hit(deck)

def hit():
    global in_play, outcome, score, current
    if in_play == True:
        player.hit(deck)

    # if the hand is in play, hit the player
        if player.busted():
            outcome = 'You went Bust! :('
            current = 'New Deal ??'
            in_play = False
            score -= 1
        if player.get_value() == 21:
            in_play = False
            outcome = 'You got BLACKJACK! :)'
            current = 'New Deal?'
            #print outcome
            score += 1
def stand():
    global outcome, in_play, score, current
    if in_play == True:
        # if hand is in play, repeatedly hit dealer until his hand has value 17 or more
        while dealer.get_value() < 17:
            dealer.hit(deck)
            if dealer.busted():
                outcome = "Dealer went Bust!"
                score += 1
        
        if not dealer.busted() and dealer.get_value() > player.get_value():
            outcome = "Dealer Won !!"
            score -= 1
            
        if not dealer.busted() and dealer.get_value() == player.get_value():
            outcome = "It's a Tie. You Lose. :("
            score -= 1
            
        if not dealer.busted() and dealer.get_value() < player.get_value():
            outcome = "You Won !!!"
            score += 1
    in_play = False
    current = "New Deal ??"
        
# draw handler    
def draw(canvas):
    global in_play
    # test to make sure that card.draw works, replace with your code below
    canvas.draw_text("BLACKJACK", (150,50), 32, 'Yellow', 'sans-serif')
    canvas.draw_text("Score: " + str(score), (200, 80), 24, 'White', 'sans-serif')
    canvas.draw_text("Dealer", (50, 100), 20, 'Black', 'sans-serif')
    canvas.draw_text("Player", (50, 300), 20, 'Black', 'sans-serif')
    canvas.draw_text(current, (160, 280), 24, 'White', 'sans-serif')
    canvas.draw_text(outcome, (160, 260), 24, 'White', 'sans-serif')
    dealer.draw(canvas, 120)
    player.draw(canvas, 320)
    card = Card("S", "A")
    if in_play:
        card.draw(canvas, 50, 120, faceDown = True)
        
# initialization frame
frame = simplegui.create_frame("Blackjack", 500, 500)
frame.set_canvas_background("Green")

#create buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
frame.set_draw_handler(draw)

# deal an initial hand
deal()

# get things rolling
frame.start()

# remember to review the gradic rubric
