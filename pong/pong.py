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


def play_pong():
    pygame.init()

    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 600
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Pong")

    # Load Background Image
    background = pygame.image.load('assets/use.png')
    background = pygame.transform.scale(
        background, (SCREEN_WIDTH, SCREEN_HEIGHT))

    WHITE = (255, 255, 255)
    RED = (255, 0, 0)  # Color for paddle1
    BLUE = (0, 0, 255)  # Color for paddle2

    # Paddle properties
    PADDLE_WIDTH = 15
    PADDLE_HEIGHT = 100
    PADDLE_SPEED = 6

    # Ball properties
    BALL_RADIUS = 7
    BALL_SPEED_X = 4
    BALL_SPEED_Y = 4

    # Initialize paddles and ball
    paddle1 = pygame.Rect(50, SCREEN_HEIGHT // 2 -
                          PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
    paddle2 = pygame.Rect(SCREEN_WIDTH - 50 - PADDLE_WIDTH, SCREEN_HEIGHT //
                          2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
    ball = pygame.Rect(SCREEN_WIDTH // 2, SCREEN_HEIGHT //
                       2, BALL_RADIUS * 2, BALL_RADIUS * 2)

    # Ball direction
    ball_speed_x = BALL_SPEED_X * random.choice((1, -1))
    ball_speed_y = BALL_SPEED_Y * random.choice((1, -1))

    # Scoring
    score_font = pygame.font.Font(None, 36)
    player1_score = 0
    player2_score = 0

    def draw_score():
        player1_score_text = score_font.render(
            f'Player 1: {player1_score}', True, WHITE)
        player2_score_text = score_font.render(
            f'Player 2: {player2_score}', True, WHITE)
        screen.blit(player1_score_text, (10, 10))
        screen.blit(player2_score_text, (SCREEN_WIDTH -
                    player2_score_text.get_width() - 10, 10))

    def draw_exit_message():
        exit_message = score_font.render('Press Space to Exit', True, WHITE)
        screen.blit(exit_message, (SCREEN_WIDTH // 2 -
                    exit_message.get_width() // 2, SCREEN_HEIGHT - 30))

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return  # Return to main menu instead of quitting the entire thing

        # Paddle Movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w] and paddle1.top > 0:
            paddle1.y -= PADDLE_SPEED
        if keys[pygame.K_s] and paddle1.bottom < SCREEN_HEIGHT:
            paddle1.y += PADDLE_SPEED
        if keys[pygame.K_UP] and paddle2.top > 0:
            paddle2.y -= PADDLE_SPEED
        if keys[pygame.K_DOWN] and paddle2.bottom < SCREEN_HEIGHT:
            paddle2.y += PADDLE_SPEED

        # Ball Movement
        ball.x += ball_speed_x
        ball.y += ball_speed_y

        # Collision with top and bottom
        if ball.top <= 0 or ball.bottom >= SCREEN_HEIGHT:
            ball_speed_y *= -1

        # Collision with paddles
        if ball.colliderect(paddle1) or ball.colliderect(paddle2):
            ball_speed_x *= -1

        # Scoring
        if ball.left <= 0:
            player2_score += 1
            ball = pygame.Rect(SCREEN_WIDTH // 2, SCREEN_HEIGHT //
                               2, BALL_RADIUS * 2, BALL_RADIUS * 2)
            ball_speed_x = BALL_SPEED_X * random.choice((1, -1))
            ball_speed_y = BALL_SPEED_Y * random.choice((1, -1))

        if ball.right >= SCREEN_WIDTH:
            player1_score += 1
            ball = pygame.Rect(SCREEN_WIDTH // 2, SCREEN_HEIGHT //
                               2, BALL_RADIUS * 2, BALL_RADIUS * 2)
            ball_speed_x = BALL_SPEED_X * random.choice((1, -1))
            ball_speed_y = BALL_SPEED_Y * random.choice((1, -1))

        screen.blit(background, (0, 0))
        pygame.draw.rect(screen, RED, paddle1)
        pygame.draw.rect(screen, BLUE, paddle2)
        pygame.draw.ellipse(screen, WHITE, ball)
        draw_score()
        draw_exit_message()

        # Update the display
        pygame.display.flip()
        pygame.time.Clock().tick(60)

    pygame.display.quit()


if __name__ == "__main__":
    play_pong()
