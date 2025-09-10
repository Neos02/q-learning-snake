import time
import pygame

from pygame.locals import *
from apple import Apple
from main import DISPLAYSURF, FONT_SMALL, WHITE, BLACK, SCREEN_WIDTH, SCREEN_HEIGHT, RED, FONT_LARGE, CLOCK, FPS, \
    TILE_WIDTH, TILE_HEIGHT
from player import Player


class Game:

    def __init__(self):
        self.apple = Apple()
        self.player = Player()
        self.survived = 0

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                    pygame.quit()

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

    def get_state(self):
        return (
            1 if self.player.velocity[0] < 0 else 0,  # moving left
            1 if self.player.velocity[1] < 0 else 0,  # moving up
            1 if self.player.velocity[0] > 0 else 0,  # moving right
            1 if self.player.velocity[1] > 0 else 0,  # moving down
            1 if self.apple.rect.left < self.player.rect.left else 0,  # apple left of snake
            1 if self.apple.rect.top < self.player.rect.top else 0,  # apple above snake
            1 if self.apple.rect.left > self.player.rect.left else 0,  # apple right of snake
            1 if self.apple.rect.top > self.player.rect.top else 0,  # apple below snake
            self._is_dangerous((-TILE_WIDTH, 0)),  # danger left
            self._is_dangerous((0, -TILE_HEIGHT)),  # danger above
            self._is_dangerous((TILE_WIDTH, 0)),  # danger right
            self._is_dangerous((0, TILE_HEIGHT))  # danger below
        )

    def step(self, action):
        reward = 0
        game_over = False

        if action == 0 and self.player.velocity[0] == 0:
            # move left
            self.player.velocity = (-TILE_WIDTH, 0)
        elif action == 1 and self.player.velocity[1] == 0:
            # move up
            self.player.velocity = (0, -TILE_HEIGHT)
        elif action == 2 and self.player.velocity[0] == 0:
            # move right
            self.player.velocity = (TILE_WIDTH, 0)
        elif action == 3 and self.player.velocity[1] == 0:
            # move down
            self.player.velocity = (0, TILE_HEIGHT)

        self.player.move()

        if pygame.sprite.collide_rect(self.player, self.apple):
            self.apple = Apple()
            self.player.length += 1
            reward = 1

        DISPLAYSURF.fill(BLACK)
        self.apple.draw(DISPLAYSURF)
        self.player.draw(DISPLAYSURF)

        score = FONT_SMALL.render("Score: " + str(self.player.length), True, WHITE)
        DISPLAYSURF.blit(score, (SCREEN_WIDTH - 100, 10))

        if self.player.is_dead():
            reward = -10
            game_over = True

        self.survived += 1

        pygame.display.update()

        return self.get_state(), reward, game_over

    def _is_dangerous(self, velocity):
        next_step = pygame.Rect(self.player.rect.left + velocity[0], self.player.rect.top + velocity[1], TILE_WIDTH, TILE_HEIGHT)

        return 1 if next_step.left < 0 or next_step.right > SCREEN_WIDTH \
                    or next_step.top < 0 or next_step.bottom > SCREEN_HEIGHT \
                    or next_step.collidelist(self.player.body) >= 0 else 0
