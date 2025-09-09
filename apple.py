import random
import pygame

from main import TILE_WIDTH, TILE_HEIGHT, ROW_COUNT, COLUMN_COUNT, RED


class Apple(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()
        self.rect = pygame.Rect(0, 0, TILE_WIDTH, TILE_HEIGHT)
        self.rect.center = (random.randint(0, COLUMN_COUNT - 1) * TILE_WIDTH + TILE_WIDTH // 2,
                            random.randint(0, ROW_COUNT - 1) * TILE_HEIGHT + TILE_HEIGHT // 2)

    def draw(self, surface):
        pygame.draw.rect(surface, RED, self.rect)