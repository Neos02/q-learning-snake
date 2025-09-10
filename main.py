import pygame
import argparse

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
    from game import Game
    from agent import Agent

    parser = argparse.ArgumentParser()
    parser.add_argument('--mode', '-m', type=int, choices=[0, 1, 2, 3], default=0, help='0 - Play Snake, 1 - Train Agent from Scratch, 2 - Continue Training Agent from Existing Model, 3 - Run Existing Model')
    parser.add_argument('--episode', '-e', type=int, help='Episode number to load')
    parser.add_argument('--model-dir', '-d', type=str, help='Directory to save and load models', default='models')
    args = parser.parse_args()

    if args.mode == 0:
        game = Game()
        game.run()
    elif args.mode == 1:
        agent = Agent(model_dir=args.model_dir)
        agent.train()
    elif args.mode == 2:
        if args.episode is None:
            parser.error('--episode must be specified')

        agent = Agent(model_dir=args.model_dir)
        agent.train_from_episode(args.episode)
    elif args.mode == 3:
        if args.episode is None:
            parser.error('--episode must be specified')

        agent = Agent(model_dir=args.model_dir)
        agent.run_episode(args.episode)
