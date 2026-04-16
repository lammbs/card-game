import random
import pygame

class Cards:
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank
    
    def hand(n):
        print("")
        

suits = ["\u2663", "\u2665", "\u2666", "\u2660"]
ranks = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]

deck = [Cards(rank, suit) for suit in suits for rank in ranks]

random.shuffle(deck)

print(deck)
