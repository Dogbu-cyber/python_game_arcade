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
import platform

import pygame
import sys
import os
import subprocess # os and subprocess to open instructions

def play_blackjack():
    from blackjack.blackjack import play_blackjack
    play_blackjack()

def play_pong():
    from pong.pong import play_pong
    play_pong()

def play_space_shooter():
    from space_shooter.space_shooter import play_space_shooter
    play_space_shooter()

def play_zombies():
    from zombies.zombies import play_zombies
    play_zombies()
def open_full_instructions(file_path):
    if os.path.isfile(file_path):
        # Open the file with the default application
        if platform.system() == 'Windows':  # For Windows
            os.startfile(file_path)
        else:
            opener = 'open' if platform.system() == 'Darwin' else 'xdg-open'  # 'open' for MacOS, 'xdg-open' for Linux
            subprocess.run([opener, file_path])
    else:
        print(f"The file {file_path} does not exist.")

def display_instructions(game):
    game = game.lower()
    open_full_instructions(f"{game.lower()}_instructions.txt")
    """ Display the instructions for the selected game. """
    instructions = {
        "blackjack": "Blackjack Instructions:\nTry to get as close to 21 without going over.\nDealer hits until they reach 17. Aces count as 1 or 11.",
        "pong": "Pong Instructions:\nPlayer 1 uses 'W' and 'S' to move.\nPlayer 2 uses Up and Down arrows.",
        "space_shooter": "Space Shooter Instructions:\nPress Space to shoot.\n Left and Right arrows to move.\nAvoid enemies and prevent them from passing you.",
        "zombies": "Zombies Instructions:\nUse arrow keys to move.\nAim and click the zombies to shoot and kill.\nAvoid taking damage from the zombies.\nPower ups: 20 kills/15 seconds increases firerate 200%.\nGet as many kills as possible before dying.\n"
    }

    SCREEN_WIDTH = 600
    SCREEN_HEIGHT = 600
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Instructions")

    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)

    font = pygame.font.SysFont('Arial', 24)
    
    # Draw instructions
    screen.fill(BLACK)
    wrapped_text = instructions[game].split('\n') + ["Enter 'start' then double press enter to begin:"]
    start_y = 100
    for line in wrapped_text:
        text = font.render(line, True, WHITE)
        text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, start_y))
        screen.blit(text, text_rect)
        start_y += 40
    pygame.display.flip()

    # Input handling
    user_input = ''
    input_box = pygame.Rect(SCREEN_WIDTH // 4, start_y + 20, SCREEN_WIDTH // 2, 40)
    pygame.draw.rect(screen, WHITE, input_box, 2)
    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    try:
                        if user_input.lower() != 'start':
                            raise ValueError("Incorrect keyword. Please enter 'start'.")
                        waiting = False
                    except ValueError as ve:
                        error_message = font.render(str(ve), True, WHITE)
                        screen.fill(BLACK, (0, start_y + 70, SCREEN_WIDTH, 40))
                        screen.blit(error_message, (50, start_y + 70))
                        pygame.display.flip()
                        user_input = ''
                        pygame.time.wait(100)
                elif event.key == pygame.K_BACKSPACE:
                    user_input = user_input[:-1]
                else:
                    user_input += event.unicode

                # Render current text in input box
                pygame.draw.rect(screen, BLACK, input_box)
                pygame.draw.rect(screen, WHITE, input_box, 2)
                text_surface = font.render(user_input, True, WHITE)
                screen.blit(text_surface, (input_box.x + 5, input_box.y + 5))
                pygame.display.flip()


    # Wait for user to acknowledge instructions
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    waiting = False

def main_menu():
    pygame.init()

    SCREEN_WIDTH = 600
    SCREEN_HEIGHT = 600
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Main Menu")

    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    LIGHT_BLUE = (173, 216, 230)
    DARK_BLUE = (0, 0, 139)
    HOVER_COLOR = (100, 149, 237)

    font = pygame.font.SysFont('comicsansms', 40)
    title_font = pygame.font.SysFont('comicsansms', 50)
    title_text = title_font.render('Game Arcade', True, LIGHT_BLUE)

    menu_options = ["Blackjack", "Pong", "Space_Shooter", 'Zombies']
    buttons = []

    for i, option in enumerate(menu_options):
        button = pygame.Rect(100, 150 + i * 70, 400, 50)
        buttons.append((button, option))

    def draw_menu(mouse_pos):
        screen.fill(BLACK)
        screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, 50))
        
        for button, text in buttons:
            if button.collidepoint(mouse_pos):
                pygame.draw.rect(screen, HOVER_COLOR, button)
            else:
                pygame.draw.rect(screen, DARK_BLUE, button)
            btn_text = font.render(text, True, WHITE)
            text_rect = btn_text.get_rect(center=button.center)
            screen.blit(btn_text, text_rect)
        pygame.display.flip()

    running = True
    while running:
        mouse_pos = pygame.mouse.get_pos()
        draw_menu(mouse_pos)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for button, game in buttons:
                    if button.collidepoint(mouse_pos):
                        display_instructions(game)
                        if game == "Blackjack":
                            play_blackjack()
                        elif game == "Pong":
                            play_pong()
                        elif game == "Space_Shooter":
                            play_space_shooter()
                        elif game == "Zombies":
                            play_zombies()

    pygame.quit()

if __name__ == "__main__":
    main_menu()


