import random
import pygame
import tkinter


# the game window
window = tkinter.Tk()
window.title("Jackblack")

# the game canvas
canvas = tkinter.Canvas(window, bg = "green", borderwidth = 0, highlightthickness =0)
canvas.pack()

window.update()

# centering the game window
window_width = window.winfo_width()
window_height = window.winfo_height()
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()


class Cards:
    suits = ["\u2663", "\u2665", "\u2666", "\u2660"]
    ranks = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]

    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank
    


window.focus_set()
window.mainloop()