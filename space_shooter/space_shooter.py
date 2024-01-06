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


def play_space_shooter():
    pygame.init()

    SCREEN_WIDTH = 600
    SCREEN_HEIGHT = 600
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Space Shooter")

    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    RED = (255, 0, 0)

    # Ship properties
    ship_speed = 7
    ship = pygame.Rect(300, 550, 60, 60)

    # Bullet properties
    bullet_speed = 7
    bullets = []

    # Enemy properties
    enemies = []
    enemy_speed = 3
    spawn_enemy_event = pygame.USEREVENT + 1
    pygame.time.set_timer(spawn_enemy_event, 2000)

    # Score
    score = 0
    font = pygame.font.SysFont(None, 36)

    exit_button = pygame.Rect(SCREEN_WIDTH - 70, 10, 60, 30)

    # Game state
    game_over = False

    # Difficulty
    difficulty_increase_interval = 20

    def draw_ship(surface, x, y):
        ship_color = (0, 0, 255)  # Blue color for the ship
        ship_points = [(x, y - 30), (x + 30, y + 30), (x - 30, y + 30)]
        pygame.draw.polygon(surface, ship_color, ship_points)

    def draw_enemy(surface, x, y):
        enemy_color = (255, 0, 0)
        pygame.draw.circle(surface, enemy_color, (x, y), 15)

    def fire_bullet():
        bullet = pygame.Rect(ship.centerx - 5, ship.top - 10, 10, 20)
        bullets.append(bullet)

    def move_bullet():
        nonlocal score
        for bullet in bullets:
            bullet.y -= bullet_speed
            if bullet.y < 0 and bullet in bullets:
                bullets.remove(bullet)
            for enemy in enemies:
                if bullet.colliderect(enemy):
                    enemies.remove(enemy)
                    if bullet in bullets:
                        bullets.remove(bullet)
                    score += 10
                    increase_difficulty()
                    break

    def spawn_enemy():
        enemy_x = random.randint(0, SCREEN_WIDTH - 30)
        enemy = pygame.Rect(enemy_x, -30, 30, 30)
        enemies.append(enemy)

    def move_enemy():
        nonlocal game_over
        for enemy in enemies:
            enemy.y += enemy_speed
            if enemy.y > SCREEN_HEIGHT:
                game_over = True  # Game over if enemy passes the bottom
                break
            if enemy.colliderect(ship):
                game_over = True  # Game over if enemy hits the ship

    def increase_difficulty():
        nonlocal enemy_speed
        if score % difficulty_increase_interval == 0:
            enemy_speed += 0.25
            pygame.time.set_timer(spawn_enemy_event, max(
                500, 2000 - (score // difficulty_increase_interval * 100)))

    def draw_score():
        score_text = font.render(f'Score: {score}', True, WHITE)
        screen.blit(score_text, (10, 10))

    def draw_exit_button():
        pygame.draw.rect(screen, WHITE, exit_button)
        exit_text = font.render('Exit', True, BLACK)
        screen.blit(exit_text, (exit_button.x + 10, exit_button.y + 5))

    def reset_game():
        nonlocal enemies, bullets, score, enemy_speed, game_over
        enemies.clear()
        bullets.clear()
        score = 0
        enemy_speed = 3
        game_over = False

    # Game loop
    running = True
    clock = pygame.time.Clock()

    while running:
        screen.fill(BLACK)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if event.type == pygame.MOUSEBUTTONDOWN:
                if exit_button.collidepoint(event.pos):
                    return  # Return to main menu instead of quitting
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if game_over:
                        reset_game()
                    else:
                        fire_bullet()
            if not game_over and event.type == spawn_enemy_event:
                spawn_enemy()

        keys = pygame.key.get_pressed()
        if not game_over:
            if keys[pygame.K_LEFT] and ship.left > 0:
                ship.x -= ship_speed
            if keys[pygame.K_RIGHT] and ship.right < SCREEN_WIDTH:
                ship.x += ship_speed

        if not game_over:
            move_bullet()
            move_enemy()

        for bullet in bullets:
            pygame.draw.rect(screen, WHITE, bullet)
        for enemy in enemies:
            draw_enemy(screen, enemy.centerx, enemy.centery)

        if not game_over:
            draw_ship(screen, ship.centerx, ship.centery)
            draw_score()
        else:
            game_over_text = font.render("Game Over", True, WHITE)
            restart_text = font.render(
                "Press Space to Play Again", True, WHITE)
            screen.blit(game_over_text, (SCREEN_WIDTH // 2 -
                        game_over_text.get_width() // 2, SCREEN_HEIGHT // 2 - 30))
            screen.blit(restart_text, (SCREEN_WIDTH // 2 -
                        restart_text.get_width() // 2, SCREEN_HEIGHT // 2 + 10))

        draw_exit_button()

        pygame.display.flip()
        clock.tick(60)

    pygame.display.quit()


if __name__ == "__main__":
    play_space_shooter()
