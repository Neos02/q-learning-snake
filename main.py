import sys
import time
import pygame

from pygame.locals import *

pygame.init()

FPS = 15
CLOCK = pygame.time.Clock()

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

FONT_SMALL = pygame.font.SysFont("Verdana", 16)
FONT_LARGE = pygame.font.SysFont("Verdana", 60)

ROW_COUNT = 32
COLUMN_COUNT = 32
TILE_WIDTH = 20
TILE_HEIGHT = 20

SCREEN_WIDTH = TILE_WIDTH * COLUMN_COUNT
SCREEN_HEIGHT = TILE_HEIGHT * ROW_COUNT

DISPLAYSURF = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Snake')

if __name__ == "__main__":
    from apple import Apple
    from player import Player

    apple = Apple()
    player = Player()

    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()

        player.move()

        if pygame.sprite.collide_rect(player, apple):
            apple = Apple()
            player.length += 1

        DISPLAYSURF.fill(BLACK)
        apple.draw(DISPLAYSURF)
        player.draw(DISPLAYSURF)

        score = FONT_SMALL.render("Score: " + str(player.length), True, WHITE)
        DISPLAYSURF.blit(score, (SCREEN_WIDTH - 100, 10))

        if player.rect.left < 0 or player.rect.right > SCREEN_WIDTH \
                or player.rect.top < 0 or player.rect.bottom > SCREEN_HEIGHT \
                or player.self_collide():
            game_over = FONT_LARGE.render("Game Over", True, WHITE)
            DISPLAYSURF.fill(RED)
            DISPLAYSURF.blit(game_over, (SCREEN_WIDTH / 2 - game_over.get_width() / 2, SCREEN_HEIGHT / 2 - game_over.get_height() / 2))

            pygame.display.update()
            time.sleep(2)
            pygame.quit()
            sys.exit()

        pygame.display.update()
        CLOCK.tick(FPS)
