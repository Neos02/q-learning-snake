import random
import sys
import time
import pygame

from pygame.locals import *
from apple import Apple
from main import DISPLAYSURF, FONT_SMALL, WHITE, BLACK, SCREEN_WIDTH, SCREEN_HEIGHT, RED, FONT_LARGE, CLOCK, FPS, \
    TILE_WIDTH, TILE_HEIGHT
from player import Player


SNAKE_VELOCITIES = [(-TILE_WIDTH, 0), (0, -TILE_HEIGHT), (TILE_WIDTH, 0), (0, TILE_HEIGHT)]


def game_over():
    game_over_text = FONT_LARGE.render("Game Over", True, WHITE)
    DISPLAYSURF.fill(RED)
    DISPLAYSURF.blit(game_over_text, (SCREEN_WIDTH / 2 - game_over_text.get_width() / 2,
                                      SCREEN_HEIGHT / 2 - game_over_text.get_height() / 2))
    pygame.display.update()
    time.sleep(2)
    pygame.quit()
    sys.exit()


class Game:

    def __init__(self, is_agent=False, draw=True):
        self.apple = Apple()
        self.player = Player(is_agent)
        self.survived = 0
        self.draw = draw

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                    pygame.quit()

            self.player.move()

            if pygame.sprite.collide_rect(self.player, self.apple):
                self.apple = Apple()
                self.player.length += 1

            self._draw()

            if self.player.is_dead():
                game_over()

            pygame.display.update()
            CLOCK.tick(FPS)

    def get_state(self):
        return (
            int(self.player.velocity[0] < 0),  # moving left
            int(self.player.velocity[1] < 0),  # moving up
            int(self.player.velocity[0] > 0),  # moving right
            int(self.player.velocity[1] > 0),  # moving down
            int(self.apple.rect.left < self.player.rect.left),  # apple left of snake
            int(self.apple.rect.top < self.player.rect.top),  # apple above snake
            int(self.apple.rect.left > self.player.rect.left),  # apple right of snake
            int(self.apple.rect.top > self.player.rect.top),  # apple below snake
            self._is_dangerous((-TILE_WIDTH, 0)),  # danger left
            self._is_dangerous((0, -TILE_HEIGHT)),  # danger above
            self._is_dangerous((TILE_WIDTH, 0)),  # danger right
            self._is_dangerous((0, TILE_HEIGHT))  # danger below
        )

    def step(self, action):
        reward = 0
        is_dead = False

        if self.player.velocity == (0, 0):
            self.player.velocity = random.choice(SNAKE_VELOCITIES)

        current_velocity_index = SNAKE_VELOCITIES.index(self.player.velocity)
        current_distance_squared = self._get_player_apple_distance_squared()

        if action == 0:
            # turn left relative to the snake
            self.player.velocity = SNAKE_VELOCITIES[(current_velocity_index - 1) % len(SNAKE_VELOCITIES)]
        elif action == 2:
            # turn right relative to the snake
            self.player.velocity = SNAKE_VELOCITIES[(current_velocity_index + 1) % len(SNAKE_VELOCITIES)]

        self.player.move()

        if self._get_player_apple_distance_squared() < current_distance_squared:
            reward = 1

        if pygame.sprite.collide_rect(self.player, self.apple):
            self.apple = Apple()
            self.player.length += 1
            reward = 10

        self._draw()

        if self.player.is_dead():
            reward = -100
            is_dead = True

        self.survived += 1

        return self.get_state(), reward, is_dead

    def _is_dangerous(self, velocity):
        next_step = pygame.Rect(self.player.rect.left + velocity[0], self.player.rect.top + velocity[1], TILE_WIDTH, TILE_HEIGHT)

        return 1 if next_step.left < 0 or next_step.right > SCREEN_WIDTH \
                    or next_step.top < 0 or next_step.bottom > SCREEN_HEIGHT \
                    or next_step.collidelist(self.player.body) >= 0 else 0

    def _draw(self):
        if not self.draw:
            return

        DISPLAYSURF.fill(BLACK)
        self.apple.draw(DISPLAYSURF)
        self.player.draw(DISPLAYSURF)

        score = FONT_SMALL.render("Score: " + str(self.player.length - self.player.start_length), True, WHITE)
        DISPLAYSURF.blit(score, (SCREEN_WIDTH - 100, 10))

        pygame.display.update()

    def _get_player_apple_distance_squared(self):
        return (self.player.rect.left - self.apple.rect.left) ** 2 + (self.player.rect.top - self.apple.rect.top) ** 2