import random
import pygame
import tkinter


class Cards:
    suits = ["\u2663", "\u2665", "\u2666", "\u2660"]
    ranks = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]

    def __init__(self):
        self.deck = [{'suit': suit, 'rank': rank} for suit in self.suits for rank in self.ranks]
    
    def shuffle(self):
        random.shuffle(self.deck)
    
    def deal(self):
        if len(self.deck) < 2:
            raise ValueError("Not enough cards to deal")
        card1 = self.deck.pop()
        card2 = self.deck.pop()
        return card1, card2
        