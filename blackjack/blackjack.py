# By submitting this assignment, I agree to the following:
#    "Aggies do not lie, cheat, or steal, or tolerate those who do."
#    "I have not given or received any unauthorized aid on this assignment."
#
# Names:        Kyle Dudley
#               Jack Hicks
#               Wyatt Baca
#               David Ogbureke
#               Jaren Belda
# Section:      473
# Assignment:   Final Project

import pygame
import random


def play_blackjack():
    pygame.init()

    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Blackjack")

    background = pygame.image.load('assets/blackjack_table.jpg')
    background = pygame.transform.scale(
        background, (800, 600))  # Scale image to fit the window
    global deck, player_cards, dealer_cards, game_over, player_turn

    WHITE = (255, 255, 255)
    RED = (255, 0, 0)
    BLACK = (0, 0, 0)

    # Card Deck
    suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
    ranks = ['2', '3', '4', '5', '6', '7', '8',
             '9', '10', 'Jack', 'Queen', 'King', 'Ace']

    # Function to create a deck of cards
    def create_deck():
        return [(rank, suit) for suit in suits for rank in ranks]

    # Function to load card images
    def load_card_images():
        card_images = {}
        for suit in suits:
            for rank in ranks:
                image_name = f"{rank.lower()}_of_{suit.lower()}.png"
                card_image = pygame.image.load(f'assets/cards/{image_name}')
                # Scale images to a suitable size
                card_image = pygame.transform.scale(card_image, (72, 96))
                card_images[(rank, suit)] = card_image
        return card_images

    def deal_card(deck):
        if len(deck) == 0:  # Check if the deck is empty (Did this to help catch bugs)
            return None
        return deck.pop()

    # Function to calculate score
    def calculate_score(cards):
        score = 0
        ace_count = 0
        for card in cards:
            rank = card[0]
            if rank in ['Jack', 'Queen', 'King']:
                score += 10
            elif rank == 'Ace':
                ace_count += 1
                score += 11
            else:
                score += int(rank)

        while score > 21 and ace_count:
            score -= 10
            ace_count -= 1

        return score

    def draw_text(text, font, color, surface, x, y):
        text_obj = font.render(text, True, color)
        text_rect = text_obj.get_rect()
        text_rect.topleft = (x, y)
        surface.blit(text_obj, text_rect)

    # Function to draw hand
    def draw_hand(hand, x, y, hide_second_card=False):
        for i, card in enumerate(hand):
            if i == 1 and hide_second_card:
                pygame.draw.rect(screen, BLACK, [x, y, 72, 96])
            else:
                screen.blit(card_images[card], (x, y))
            x += 80  # Offset each card so they don't overlap entirely

    # Function to reset the game
    def reset_game():
        global deck, player_cards, dealer_cards, game_over, player_turn
        deck = create_deck()
        random.shuffle(deck)
        player_cards = [deal_card(deck), deal_card(deck)]
        dealer_cards = [deal_card(deck), deal_card(deck)]
        game_over = False
        player_turn = True

    # Button class
    class Button:
        def __init__(self, text, x, y, width, height, font, color, highlight_color):
            self.text = text
            self.x = x
            self.y = y
            self.width = width
            self.height = height
            self.font = font
            self.color = color
            self.highlight_color = highlight_color

        def draw(self, screen, mouse_pos):
            if self.x <= mouse_pos[0] <= self.x + self.width and self.y <= mouse_pos[1] <= self.y + self.height:
                pygame.draw.rect(screen, self.highlight_color, [
                                 self.x, self.y, self.width, self.height])
            else:
                pygame.draw.rect(screen, self.color, [
                                 self.x, self.y, self.width, self.height])

            text_surface = self.font.render(self.text, True, BLACK)
            screen.blit(text_surface, (self.x + 10, self.y + 10))

        def is_over(self, mouse_pos):
            return self.x <= mouse_pos[0] <= self.x + self.width and self.y <= mouse_pos[1] <= self.y + self.height

    # Load card images
    card_images = load_card_images()

    font = pygame.font.SysFont(None, 36)
    hit_button = Button("Hit", 650, 500, 100, 40, font, RED, WHITE)
    stand_button = Button("Stand", 650, 550, 100, 40, font, RED, WHITE)
    play_again_button = Button(
        "Play Again", 300, 300, 150, 50, font, RED, WHITE)
    exit_button = Button("Exit", 700, 10, 80, 40, font,
                         RED, WHITE)  

    # Initial Game Setup
    reset_game()

    # Game Loop
    running = True
    while running:
        mouse_pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if exit_button.is_over(mouse_pos):
                    return  # Return to the main menu
                if play_again_button.is_over(mouse_pos) and game_over:
                    reset_game()
                if hit_button.is_over(mouse_pos) and not game_over and player_turn:
                    player_cards.append(deal_card(deck))
                    player_score = calculate_score(player_cards)
                    if player_score >= 21:
                        player_turn = False
                        game_over = True
                if stand_button.is_over(mouse_pos) and not game_over and player_turn:
                    player_turn = False

        player_score = calculate_score(player_cards)
        dealer_score = calculate_score(dealer_cards)

        # Dealer's Play
        if not player_turn and not game_over:
            while dealer_score < 17:
                dealer_cards.append(deal_card(deck))
                dealer_score = calculate_score(dealer_cards)
            game_over = True

        # Render Background
        screen.blit(background, (0, 0))

        # Draw Buttons
        hit_button.draw(screen, mouse_pos)
        stand_button.draw(screen, mouse_pos)
        exit_button.draw(screen, mouse_pos)
        if game_over:
            play_again_button.draw(screen, mouse_pos)

        # Draw Hands
        draw_hand(player_cards, 50, 400, hide_second_card=False)
        draw_hand(dealer_cards, 50, 100, hide_second_card=not game_over)

        # Display Scores
        draw_text(f"Player: {player_score}", font, WHITE, screen, 50, 500)
        draw_text(
            f"Dealer: {'?' if not game_over else dealer_score}", font, WHITE, screen, 50, 50)

        # Display Result
        if game_over:
            if player_score > 21:
                draw_text("Dealer wins!", font, WHITE, screen, 300, 250)
            elif dealer_score > 21 or player_score > dealer_score:
                draw_text("Player wins!", font, WHITE, screen, 300, 250)
            elif player_score == dealer_score:
                draw_text("It's a draw!", font, WHITE, screen, 300, 250)
            else:
                draw_text("Dealer wins!", font, WHITE, screen, 300, 250)

        # Update the Display
        pygame.display.update()


if __name__ == "__main__":
    play_blackjack()
