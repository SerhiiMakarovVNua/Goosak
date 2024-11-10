import pygame
import random
import os
from pygame.constants import QUIT, K_s, K_w, K_a, K_d

pygame.init()

FPS = pygame.time.Clock()

WIDTH = 1000
HEIGHT = 600

FONT = pygame.font.SysFont('Verdana', 20)
FONT_LARGE = pygame.font.SysFont('Verdana', 40)  # Шрифт для Game Over

COLOR_BLACK = (0, 0, 0)
COLOR_RED = (255, 0, 0)

main_display = pygame.display.set_mode((WIDTH, HEIGHT))

bg = pygame.transform.scale(pygame.image.load('background.png'), (WIDTH, HEIGHT))
bg_X1 = 0
bg_X2 = bg.get_width()
bg_move = 2

IMAGE_PATH = "Goose"
PLAYER_IMAGES = os.listdir(IMAGE_PATH)

player_size = (20, 20)
player = pygame.image.load('player.png').convert_alpha()
player_rect = player.get_rect(center=(200, HEIGHT // 2))

player_move_down = [0, 3]
player_move_right = [3, 0]
player_move_up = [0, -3]
player_move_left = [-3, 0]

def create_enemy():
    enemy_size = (30, 30)
    enemy = pygame.image.load('enemy.png').convert_alpha()
    enemy_rect = pygame.Rect(WIDTH, random.randint(100, HEIGHT-100), *enemy_size)
    enemy_move = [random.randint(-6, -3), 0]
    return [enemy, enemy_rect, enemy_move]

def create_bonus():
    bonus_size = (25, 25)
    bonus = pygame.image.load('bonus.png').convert_alpha()
    bonus_rect = pygame.Rect(random.randint(300, WIDTH-150), 0, *bonus_size)
    bonus_move = [0, random.randint(3, 6)]
    return [bonus, bonus_rect, bonus_move]

CREATE_ENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(CREATE_ENEMY, 3000)
CREATE_BONUS = pygame.USEREVENT + 2
pygame.time.set_timer(CREATE_BONUS, 2000)
CHANGE_IMAGE = pygame.USEREVENT + 3
pygame.time.set_timer(CHANGE_IMAGE, 200)

enemies = []
bonuses = []

score = 0
image_index = 0

playing = True
game_over = False  # Стан гри (чи гра закінчена)

while playing:
    FPS.tick(120)
    for event in pygame.event.get():
        if event.type == QUIT:
            playing = False
        if event.type == CREATE_ENEMY and not game_over:
            enemies.append(create_enemy())
        if event.type == CREATE_BONUS and not game_over:
            bonuses.append(create_bonus())
        if event.type == CHANGE_IMAGE and not game_over:
            player = pygame.image.load(os.path.join(IMAGE_PATH, PLAYER_IMAGES[image_index]))
            image_index += 1
            if image_index >= len(PLAYER_IMAGES):
                image_index = 0    

    # Якщо гра закінчена, не рухати фон
    if not game_over:
        bg_X1 -= bg_move
        bg_X2 -= bg_move

        if bg_X1 < -bg.get_width():
            bg_X1 = bg.get_width()

        if bg_X2 < -bg.get_width():
            bg_X2 = bg.get_width()

    main_display.blit(bg, (bg_X1, 0))
    main_display.blit(bg, (bg_X2, 0))

    if not game_over:
        keys = pygame.key.get_pressed()

        if keys[K_s] and player_rect.bottom < HEIGHT:
            player_rect = player_rect.move(player_move_down)

        if keys[K_d] and player_rect.right < WIDTH:
            player_rect = player_rect.move(player_move_right)

        if keys[K_w] and player_rect.top > 0:
            player_rect = player_rect.move(player_move_up)

        if keys[K_a] and player_rect.left > 0:
            player_rect = player_rect.move(player_move_left)

        for enemy in enemies:
            enemy[1] = enemy[1].move(enemy[2])
            main_display.blit(enemy[0], enemy[1])

            if player_rect.colliderect(enemy[1]):
                game_over = True  # Якщо зіткнення, гра закінчується

        for bonus in bonuses:
            bonus[1] = bonus[1].move(bonus[2])
            main_display.blit(bonus[0], bonus[1])

            if player_rect.colliderect(bonus[1]):
                score += 1
                bonuses.pop(bonuses.index(bonus))

        main_display.blit(FONT.render(str(score), True, COLOR_BLACK), (WIDTH-50, 20))
        main_display.blit(player, player_rect) 

    # Показати екран Game Over
    if game_over:
        game_over_text = FONT_LARGE.render("GAME OVER", True, COLOR_RED)
        score_text = FONT.render(f"Final Score: {score}", True, COLOR_BLACK)
        main_display.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2 - 50))
        main_display.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, HEIGHT // 2 + 10))

    pygame.display.flip()

    # Очищення ворогів і бонусів, якщо вони вийшли за межі екрану
    for enemy in enemies:
        if enemy[1].left < 0:
            enemies.pop(enemies.index(enemy))

    for bonus in bonuses:
        if bonus[1].bottom > HEIGHT:
            bonuses.pop(bonuses.index(bonus))

pygame.quit()
