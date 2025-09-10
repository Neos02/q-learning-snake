import pygame

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
    from agent import Agent
    agent = Agent()
    agent.train_from_episode(7500)
