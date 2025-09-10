import pygame

from pygame.locals import *
from main import TILE_WIDTH, TILE_HEIGHT, GREEN, SCREEN_WIDTH, SCREEN_HEIGHT, ROW_COUNT, COLUMN_COUNT


class Player(pygame.sprite.Sprite):

    def __init__(self, is_agent=False):
        super().__init__()
        self.body = [pygame.Rect(TILE_WIDTH * COLUMN_COUNT // 2, TILE_HEIGHT * ROW_COUNT // 2, TILE_WIDTH, TILE_HEIGHT)]
        self.rect = self.body[0]
        self.velocity = (0, 0)
        self.length = 5
        self.is_agent = is_agent

    def move(self):
        pressed_keys = pygame.key.get_pressed()

        if not self.is_agent:
            if self.velocity[0] == 0:
                if pressed_keys[K_a]:
                    self.velocity = (-TILE_WIDTH, 0)

                if pressed_keys[K_d]:
                    self.velocity = (TILE_WIDTH, 0)

            if self.velocity[1] == 0:
                if pressed_keys[K_w]:
                    self.velocity = (0, -TILE_HEIGHT)

                if pressed_keys[K_s]:
                    self.velocity = (0, TILE_HEIGHT)

        if self.velocity != (0, 0):
            self.add_segment()

        if len(self.body) > self.length:
            self.body.pop(len(self.body) - 1)

        self.rect = self.body[0]

    def draw(self, surface):
        for rect in self.body:
            pygame.draw.rect(surface, GREEN, rect)

    def add_segment(self):
        self.body.insert(0, pygame.Rect(self.body[0].left + self.velocity[0], self.body[0].top + self.velocity[1], TILE_WIDTH, TILE_HEIGHT))

    def is_dead(self):
        return self.rect.left < 0 or self.rect.right > SCREEN_WIDTH \
            or self.rect.top < 0 or self.rect.bottom > SCREEN_HEIGHT \
            or self._self_collide()

    def _self_collide(self):
        return len(self.body) > 1 and self.rect.collidelist(self.body[1:]) >= 0
