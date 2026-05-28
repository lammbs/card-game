import random
import copy
import pygame
import blackjack_buttons
# the game window
pygame.init()
window = pygame.display.set_mode((1920,1200), pygame.RESIZABLE)
pygame.display.set_caption("Jackass")
font = pygame.font.SysFont("Arial", 50)
smaller_font = pygame.font.SysFont("Arial", 45)
# images
title = pygame.image.load("img/Skjermbilde_2026-04-30_091201-removebg-preview.png").convert_alpha()
playbutton = pygame.image.load("img/play-button-icon-png-5-removebg-preview.png").convert_alpha()
exitbutton = pygame.image.load("img/3E0657-1PTE-removebg-preview.png").convert_alpha()
backbutton = pygame.image.load("img/pngtree-blue-round-crystal-button-return-icon-png-image_4405424.png").convert_alpha()
# game class
class jackblack():
    def __init__(self):
        self.active = False
        self.records = [0, 0, 0]
        self.player_score = 0
        self.dealer_score = 0
        self.my_hand = []
        self.dealer_hand = []
        self.initial_deal = True
        self.outcome = 0
        self.reveal_dealer = False
        self.hand_active = False
        self.add_score = False
        self.results = ['', 'PLAYER BUSTED o_O', 'Player WINS! :)', 'DEALER WINS :(', 'TIE GAME...']
    # dealing the cards and removing them from the deck
    def deal_cards(self, current_hand, current_deck):
        card_index = random.randrange(len(current_deck))
        current_hand.append(current_deck.pop(card_index))
        return current_hand, current_deck
    # drawing the scores
    def draw_scores(self, player, dealer):
        window.blit(font.render(f'Score[{player}]', True, 'white'), (1600, 600))
        if self.reveal_dealer:
            window.blit(font.render(f'Score[{dealer}]', True, 'white'), (1600, 400))
    # draw the cards
    def draw_cards(self, player, dealer, reveal):
        for i in range(len(player)):
            pygame.draw.rect(window, 'white', [720 + (70 * i), 650 + (5 * i), 150, 225], 0, 5)
            window.blit(smaller_font.render(player[i], True, 'black'), (726 + 70 * i, 650 + 5 * i))
            window.blit(smaller_font.render(player[i], True, 'black'), (726 + 70 * i, 820 + 5 * i))
            pygame.draw.rect(window, 'red', [720 + (70 * i), 650 + (5 * i), 150, 225], 5, 5)
        for i in range(len(dealer)):
            pygame.draw.rect(window, 'white', [720 + (70 * i), 160 + (5 * i), 150, 225], 0, 5)
            if i != 0 or reveal:
                window.blit(smaller_font.render(dealer[i], True, 'black'), (725 + 70 * i, 165 + 5 * i))
                window.blit(smaller_font.render(dealer[i], True, 'black'), (725 + 70 * i, 330 + 5 * i))
            else:
                window.blit(smaller_font.render('???', True, 'black'), (725 + 70 * i, 165 + 5 * i))
                window.blit(smaller_font.render('???', True, 'black'), (725 + 70 * i, 330 + 5 * i))
            pygame.draw.rect(window, 'blue', [720 + (70 * i), 160 + (5 * i), 150, 225], 5, 5)
    # calculating the score of player and dealers hand
    def calculate_score(self, hand):
        hand_score = 0
        aces_count = hand.count('A')
        for i in range(len(hand)):
            for j in range(8):
                if hand[i] == cards[j]:
                    hand_score += int(hand[i])
            if hand[i] in ['10', 'J', 'Q', 'K']:
                hand_score += 10
            elif hand[i] == 'A':
                hand_score += 11
        if hand_score > 21 and aces_count > 0:
            for i in range(aces_count):
                if hand_score > 21:
                    hand_score -= 10
        return hand_score
    # draw game conditions and buttons
    def draw_game(self, act, record, outcome):
        button_list = []
        if not act:
            deal = pygame.draw.rect(window, 'white', [760, 580, 300, 100], 0, 5)
            pygame.draw.rect(window, 'green', [760, 580, 300, 100], 3, 5)
            deal_text = font.render('DEAL HAND', True, 'black')
            window.blit(deal_text, (792, 600))
            button_list.append(deal)
        else:
            hit = pygame.draw.rect(window, 'white', [610, 1000, 300, 100], 0, 5)
            pygame.draw.rect(window, 'green', [610, 1000, 300, 100], 3, 5)
            hit_text = font.render('HIT ME', True, 'black')
            window.blit(hit_text, (690, 1023))
            button_list.append(hit)
            stand = pygame.draw.rect(window, 'white', [910, 1000, 300, 100], 0, 5)
            pygame.draw.rect(window, 'green', [910, 1000, 300, 100], 3, 5)
            stand_text = font.render('STAND', True, 'black')
            window.blit(stand_text, (990, 1023))
            button_list.append(stand)
            score_text = font.render(f'Wins: {record[0]}   Losses: {record[1]}   Draws: {record[2]}', True, 'white')
            window.blit(score_text, (30, 100))
        if outcome != 0:
            window.blit(font.render(self.results[outcome], True, 'white'), (1450, 100))
            deal = pygame.draw.rect(window, 'white', [760, 480, 300, 100], 0, 5)
            pygame.draw.rect(window, 'green', [760, 480, 300, 100], 3, 5)
            pygame.draw.rect(window, 'black', [763, 483, 294, 94], 3, 5)
            deal_text = font.render('NEW HAND', True, 'black')
            window.blit(deal_text, (800, 500))
            button_list.append(deal)
        return button_list
    # draw the start screen and play button
    def draw_start_screen(self):
        window.blit(title, (400, 15))
        exit = blackjack_buttons.Buttons(1841, 1121, exitbutton, 0.159)
        play = blackjack_buttons.Buttons(440, 200, playbutton, 1.9)
        return play, exit
    # checking the results
    def check_endgame(self, hand_act, deal_score, play_score, outcome, totals, add):
        if not hand_act and deal_score >= 17:
            if play_score > 21:
                outcome = 1
            elif deal_score < play_score <= 21 or deal_score > 21:
                outcome = 2
            elif play_score < deal_score <= 21:
                outcome = 3
            else:
                outcome = 4
            if add:
                if outcome == 1 or outcome == 3:
                    totals[1] += 1
                elif outcome == 2:
                    totals[0] += 1
                else:
                    totals[2] += 1
                add = False
        return outcome, totals, add
# cards
cards = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
one_deck = 4 * cards
decks = 4
game_deck = copy.deepcopy(decks * one_deck)
# create game instance and initialize state
game = jackblack()
run = True
active = False
initial_deal = False
my_hand = []
dealer_hand = []
records = [0, 0, 0]
outcome = 0
reveal_dealer = False
hand_active = False
add_score = False
player_score = 0
dealer_score = 0
show_start_screen = True
# main game loop
while run:
    window.fill((43, 130, 57))
    if show_start_screen:
        play, exit = game.draw_start_screen()
        buttons = []
        if play.draw(window):
            show_start_screen = False
            active = True
            initial_deal = True
            game_deck = copy.deepcopy(decks * one_deck)
            my_hand = []
            dealer_hand = []
            outcome = 0
            hand_active = True
            reveal_dealer = False
            add_score = True
            player_score = 0
            dealer_score = 0
        if exit.draw(window):
            run = False
    else:
        if active and initial_deal:
            for i in range(2):
                my_hand, game_deck = game.deal_cards(my_hand, game_deck)
                dealer_hand, game_deck = game.deal_cards(dealer_hand, game_deck)
            initial_deal = False
        if active:
            player_score = game.calculate_score(my_hand)
            if reveal_dealer:
                dealer_score = game.calculate_score(dealer_hand)
                while dealer_score < 17:
                    dealer_hand, game_deck = game.deal_cards(dealer_hand, game_deck)
                    dealer_score = game.calculate_score(dealer_hand)
            game.draw_cards(my_hand, dealer_hand, reveal_dealer)
            game.draw_scores(player_score, dealer_score)
        else:
            dealer_score = 0

        buttons = game.draw_game(active, records, outcome)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONUP and buttons and not show_start_screen:
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
                    add_score = True
                    player_score = 0
                    dealer_score = 0
            else:
                if buttons[0].collidepoint(event.pos) and player_score < 21 and hand_active:
                    my_hand, game_deck = game.deal_cards(my_hand, game_deck)
                elif buttons[1].collidepoint(event.pos) and not reveal_dealer:
                    reveal_dealer = True
                    hand_active = False
                elif len(buttons) == 3 and buttons[2].collidepoint(event.pos):
                    active = True
                    initial_deal = True
                    game_deck = copy.deepcopy(decks * one_deck)
                    my_hand = []
                    dealer_hand = []
                    outcome = 0
                    hand_active = True
                    reveal_dealer = False
                    add_score = True
                    dealer_score = 0
                    player_score = 0
    if active and hand_active and player_score >= 21:
        hand_active = False
        reveal_dealer = True
    outcome, records, add_score = game.check_endgame(hand_active, dealer_score, player_score, outcome, records, add_score)
    pygame.display.flip()
pygame.quit()