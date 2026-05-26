import random
import copy
import pygame
import blackjack_deck
import blackjack_player
import blackjack_buttons

# The game window
pygame.init()
window = pygame.display.set_mode((1920,1200), pygame.RESIZABLE)
pygame.display.set_caption("Jackass")
font = pygame.font.SysFont("Arial", 50)
action = True
records = [0, 0, 0]
player_score = 0
dealer_score = 0
my_hand = []
dealer_hand = []
initial_deal = True
outcome = 0

# Images
title = pygame.image.load("img/Skjermbilde_2026-04-30_091201-removebg-preview.png").convert_alpha()
playbutton = pygame.image.load("img/play-button-icon-png-5-removebg-preview.png").convert_alpha()
rules = pygame.image.load("img/466-4660322_rules-test-rules-icon-transparent-background-removebg-preview.png").convert_alpha()
exitbutton = pygame.image.load("img/3E0657-1PTE-removebg-preview.png").convert_alpha()
ruleimg = pygame.image.load("img/import-illustrator-image.pygame_rules.png").convert_alpha()
returnbutton = pygame.image.load("img/pngtree-blue-round-crystal-button-return-icon-png-image_4405424.png").convert_alpha()

# Buttons: position and scaling
playbutton = blackjack_buttons.Buttons(500, 270, playbutton, 1.8)
rules = blackjack_buttons.Buttons(-10, 950, rules, 0.5)
exitbutton = blackjack_buttons.Buttons(1820, 1100, exitbutton, 0.199)
returnbutton = blackjack_buttons.Buttons(10, 1100, returnbutton, 0.5)

def show_rules():
    window.fill((43, 130, 57))
    window.blit(ruleimg, (500, 50))
    pygame.display.update()

def deal_cards(hand, deck):
    card = deck.deck.pop()
    hand.append(card)
    return hand, deck

def draw_game(act, records):
    window.fill((43, 130, 57))
    button_list = []

    if not act:
        deal = pygame.draw.rect(window, "white", [150, 20, 300, 100], 0, 5)
        pygame.draw.rect(window, "dark green", [150, 20, 300, 100], 3, 5)
        deal_text = font.render("DEAL HAND", True, "black")
        window.blit(deal_text, (165, 50))
        button_list.append(deal)

    else:
        hit = pygame.draw.rect(window, "white", [500, 700, 300, 100], 0, 5)
        pygame.draw.rect(window, "dark green", [500, 700, 300, 100], 3, 5)
        hit_text = font.render("HIT ME", True, "black")
        window.blit(hit_text, (515, 720))
        button_list.append(hit)

        stand = pygame.draw.rect(window, "white", [300, 700, 300, 100], 0, 5)
        pygame.draw.rect(window, "dark green", [300, 700, 300, 100], 3, 5)
        stand_text = font.render("STAND", True, "black")
        window.blit(stand_text, (315, 720))
        button_list.append(stand)
        score_text = font.render(f"Wins: {records[0]} | Losses: {records[1]} | Ties: {records[2]}", True, "black")
        window.blit(score_text, (165, 60))

    return button_list


# Game loop
run = True
while run:
    pygame.time.delay(60)

    # Background color
    window.fill((43, 130, 57))

    # Display images
    window.blit(title, (400, 50))

    if initial_deal:
        for i in range(2):
            my_hand, game_cards = deal_cards(my_hand, game_cards)
            dealer_hand, game_cards = deal_cards(dealer_hand, game_cards)
        initial_deal = False

    buttons = draw_game(action, records)

    if playbutton.draw(window):
        draw_game(action, records)
    if rules.draw(window):
        show_rules()
    if exitbutton.draw(window):
        run = False


    # Event handler
    for event in pygame.event.get():
        # Quit game
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONUP:
            if not action:
                if buttons[0].collidepoint(event.pos):
                    action = True
                    initial_deal = True
                    my_hand = []
                    dealer_hand = []

    pygame.display.flip()

pygame.quit()
