import random
import pygame
import blackjack_deck
import blackjack_player
import blackjack_buttons

# The game window
pygame.init()
window = pygame.display.set_mode((1920,1200), pygame.RESIZABLE)
pygame.display.set_caption("Jackass")

# Images
title = pygame.image.load("img/Skjermbilde_2026-04-30_091201-removebg-preview.png").convert_alpha()
playbutton = pygame.image.load("img/play-button-icon-png-5-removebg-preview.png").convert_alpha()
rules = pygame.image.load("img/466-4660322_rules-test-rules-icon-transparent-background-removebg-preview.png").convert_alpha()
exitbutton = pygame.image.load("img/3E0657-1PTE-removebg-preview.png").convert_alpha()


playbutton = blackjack_buttons.Buttons(500, 270, playbutton, 1.8)
rules = blackjack_buttons.Buttons(-10, 1100, rules, 0.222)
exitbutton = blackjack_buttons.Buttons(1820, 1100, exitbutton, 0.199)

# Game loop
run = True
while run:
    pygame.time.delay(60)

    # Background color
    window.fill((43, 130, 57))

    # Display images
    window.blit(title, (400, 50))

    if playbutton.draw(window):
        print("Play button clicked")
    rules.draw(window)
    if exitbutton.draw(window):
        run = False


    # Event handler
    for event in pygame.event.get():
        # Quit game
        if event.type == pygame.QUIT:
            run = False


        pygame.display.update()

pygame.quit()
