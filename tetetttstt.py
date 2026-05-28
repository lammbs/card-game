import random
import copy
import pygame
import blackjack_buttons

# The game window
pygame.init()
window = pygame.display.set_mode((1920,1200), pygame.RESIZABLE)
pygame.display.set_caption("Jackass")
font = pygame.font.SysFont("Arial", 50)

# game variables
active = False
records = [0, 0, 0]
player_score = 0
dealer_score = 0
my_hand = []
dealer_hand = []
initial_deal = True
outcome = 0
reveal_dealer = False
hand_active = False
add_score = False
results = ['', 'PLAYER BUSTED o_O', 'Player WINS! :)', 'DEALER WINS :(', 'TIE GAME...']

#cards 
cards = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
one_deck = 4 * cards
decks = 4
game_deck = copy.deepcopy(decks * one_deck)

# Images
title = pygame.image.load("img/Skjermbilde_2026-04-30_091201-removebg-preview.png").convert_alpha()
playbutton = pygame.image.load("img/play-button-icon-png-5-removebg-preview.png").convert_alpha()
exitbutton = pygame.image.load("img/3E0657-1PTE-removebg-preview.png").convert_alpha()

# Buttons: position and scaling
playbutton = blackjack_buttons.Buttons(500, 270, playbutton, 1.8)
exitbutton = blackjack_buttons.Buttons(1820, 1100, exitbutton, 0.199)

# deal cards
def deal_cards(current_hand, current_deck):
    card = random.randint(0, len(current_deck))
    current_hand.append(current_deck[card - 1])
    current_deck.pop(card - 1)
    return current_hand, current_deck

# score display
def draw_scores(player, dealer):
    window.blit(font.render(f"Score[{player}]", True, "white"), (350, 400))
    if reveal_dealer:
        window.blit(font.render(f"Score[{dealer}]", True, "white"), (350, 100))


# drawing cars visually
def draw_cards(player, dealer, reveal):
    for i in range(len(player)):
        pygame.draw.rect(window, "white", [70 + (70 *i), 460,  + (5 * i), 220, 260], 0, 5)
        window.blit(font.render(player[i], True, "black"), (75 + 70*i, 465 + 5*i))
        window.blit(font.render(player[i], True, "black"), (75 + 70*i, 665 + 5*i))
        pygame.draw.rect(window, "red", [70 + (70 *i), 460,  + (5 * i), 120, 220], 5, 5)

    # dealer hides one card
    for i in range(len(dealer)):
        pygame.draw.rect(window, "white", [70 + (70 *i), 160,  + (5 * i), 220, 260], 0, 5)
        if i != 0 or reveal:
            window.blit(font.render(dealer[i], True, "black"), (75 + 70*i, 165 + 5*i))
            window.blit(font.render(dealer[i], True, "black"), (75 + 70*i, 365 + 5*i))
        else:
            window.blit(font.render("?", True, "black"), (75 + 70*i, 165 + 5*i))
            window.blit(font.render("?", True, "black"), (75 + 70*i, 365 + 5*i))
        pygame.draw.rect(window, "blue", [70 + (70 *i), 160,  + (5 * i), 120, 220], 5, 5)



# calculate score of hand
def calculate_score(hand):
    hand_score = 0
    aces_count = hand.count("A")
    for i in range(len(hand)):
        for j in range(8):
            if hand[i] == cards[j]:
                hand_score += int(hand[i])
        if hand[i] in ["10", "J", "Q", "K"]:
            hand_score += 10
        elif hand[i] == "A":
            hand_score += 11
    if hand_score > 21 and aces_count > 0:
        for i in range(aces_count):
            if hand_score > 21:
                hand_score -= 10
    return hand_score

# game logic
def draw_game(act, record, results):
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
        score_text = font.render(f"Wins: {record[0]} | Losses: {record[1]} | Ties: {record[2]}", True, "black")
        window.blit(score_text, (165, 60))
        if outcome != 0:
            window.blit(font.render(results[results], True, "black"), (165, 140))
            deal = pygame.draw.rect(window, "white", [150, 220, 300, 100], 0, 5)
            pygame.draw.rect(window, "green", [150, 220, 300, 100], 3, 5)
            pygame.draw.rect(window, "black", [153, 223, 294, 94], 3, 5)
            deal_text = font.render("TRY AGAIN?", True, "black")
            window.blit(deal_text, (165, 250))
            button_list.append(deal)
    return button_list

# check for win or loss
def check_endgame(hand_active, dealer_score, player_score, outcome, totals, add):
    # player blackjacks, stands or busts
    if not hand_active and dealer_score >= 17:
        if player_score > 21:
            results = 1
        elif dealer_score < player_score <= 21 or dealer_score > 21:
            results = 2
        elif player_score < dealer_score <= 21:
            results = 3
        else:
            results = 4
        if add:
            if outcome == 1 or outcome == 3:
                totals[1] += 1 
            elif outcome == 2:
                totals[0] += 1
            else: totals[2] += 1
            add = False
    return outcome, totals, add


# game loop
run = True
while run:
    pygame.time.delay(60)
    window.fill((43, 130, 57))
    window.blit(title, (400, 50))

    if initial_deal:
        for i in range(2):
            my_hand, game_deck = deal_cards(my_hand, game_deck)
            dealer_hand, game_deck = deal_cards(dealer_hand, game_deck)
        initial_deal = False

    if active:
        player_score = calculate_score(my_hand)
        draw_cards(my_hand, dealer_hand, reveal_dealer)
        if reveal_dealer:
            dealer_score = calculate_score(dealer_hand)
            if dealer_score < 17:
                dealer_hand, game_deck = deal_cards(dealer_hand, game_deck)
        draw_scores(player_score, dealer_score)
    buttons = draw_game(active, records, outcome)
    if playbutton.draw(window):
        draw_game(active, records, outcome)

    if exitbutton.draw(window):
        run = False


    # Event handler
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONUP:
            if not active:
                if buttons[0].collidepoint(event.pos):
                    active = True
                    initial_deal = True
                    game_deck = copy.deepcopy(decks * one_deck)
                    my_hand = []
                    dealer_hand = []
                    outcome = 0
                    hand_active = True
                    reveal_dealer = False
                    outcome = 0
                    add_score = True
            else:
                if buttons[0].collidepoint(event.pos) and player_score < 21 and hand_active:
                    my_hand, game_deck = deal_cards(my_hand, game_deck)
                elif buttons[1].collidepoint(event.pos) and not reveal_dealer:
                    reveal_dealer = True
                    hand_active = False
                elif len(buttons) == 3:
                    if buttons[2].collidepoint(event.pos):
                        active = True
                        initial_deal = True
                        my_hand = []
                        dealer_hand = []
                        game_deck = copy.deepcopy(decks * one_deck)
                        outcome = 0
                        hand_active = True
                        reveal_dealer = False
                        outcome = 0
                        add_score = True
                        dealer_score = 0
                        player_score = 0

    if hand_active and player_score >= 21:
        hand_active = False
        reveal_dealer = True


    outcome, records, add_score = check_endgame(hand_active, dealer_score, player_score, outcome, records, add_score)

    pygame.display.flip()

pygame.quit()
