import sys
import time

import pygame

from pygame.locals import *
from apple import Apple
from main import DISPLAYSURF, FONT_SMALL, WHITE, BLACK, SCREEN_WIDTH, SCREEN_HEIGHT, RED, FONT_LARGE, CLOCK, FPS
from player import Player


class Game:

    def __init__(self):
        self.apple = Apple()
        self.player = Player()

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                    pygame.quit()
                    sys.exit()

            self.player.move()

            if pygame.sprite.collide_rect(self.player, self.apple):
                self.apple = Apple()
                self.player.length += 1

            DISPLAYSURF.fill(BLACK)
            self.apple.draw(DISPLAYSURF)
            self.player.draw(DISPLAYSURF)

            score = FONT_SMALL.render("Score: " + str(self.player.length), True, WHITE)
            DISPLAYSURF.blit(score, (SCREEN_WIDTH - 100, 10))

            if self.player.is_dead():
                self.game_over()

            pygame.display.update()
            CLOCK.tick(FPS)

    def game_over(self):
        game_over_text = FONT_LARGE.render("Game Over", True, WHITE)
        DISPLAYSURF.fill(RED)
        DISPLAYSURF.blit(game_over_text, (SCREEN_WIDTH / 2 - game_over_text.get_width() / 2,
                                          SCREEN_HEIGHT / 2 - game_over_text.get_height() / 2))
        pygame.display.update()
        time.sleep(2)
        pygame.quit()
        sys.exit()
