import random
import sys

import numpy as np
import pygame
import pickle

from pygame.locals import *
from game import Game
from main import CLOCK, FPS


class Agent:

    def __init__(self):
        self.discount_rate = 0.95
        self.learning_rate = 0.01
        self.epsilon = 1.0
        self.epsilon_discount = 0.9992
        self.min_epsilon = 0.001
        self.num_episodes = 10000
        self.table = np.zeros((2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 4))
        self.game = Game()
        self.score = []
        self.survived = []

    def get_action(self, state):
        # select random action (exploration)
        if random.random() < self.epsilon:
            return random.choice([0, 1, 2, 3])

        # select best action (exploitation)
        return np.argmax(self.table[state])

    def train_from_episode(self, episode=1):
        self._load_model(episode)
        self.train(episode)

    def train(self, episode=1):
        for i in range(episode, self.num_episodes):
            self.game = Game()
            steps_without_food = 0
            length = self.game.player.length

            # print updates
            if i % 25 == 0 and len(self.score) > 0:
                print(
                    f"Episodes: {i}, score: {np.mean(self.score)}, survived: {np.mean(self.survived)}, epsilon: {self.epsilon}, learning_rate: {self.learning_rate}")
                self.score = []
                self.survived = []

            # occasionally save latest model
            if (i < 100 and i % 10 == 0) or (100 <= i < 1000 and i % 200 == 0) or (i >= 1000 and i % 500 == 0):
                with open(f'pickle/snake_model_{i}.pickle', 'wb') as file:
                    pickle.dump(self.table, file)

            current_state = self.game.get_state()
            self.epsilon = max(self.epsilon * self.epsilon_discount, self.min_epsilon)

            done = False
            while not done:
                for event in pygame.event.get():
                    if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                        pygame.quit()
                        sys.exit()

                # choose action and take it
                action = self.get_action(current_state)
                new_state, reward, done = self.game.step(action)

                # Bellman equation update
                self.table[current_state][action] = (1 - self.learning_rate) \
                                                    * self.table[current_state][action] + self.learning_rate \
                                                    * (reward + self.discount_rate * max(self.table[new_state]))
                current_state = new_state

                if i % 100 == 0:
                    CLOCK.tick(FPS)

                steps_without_food += 1

                # prevent infinite loops
                if length != self.game.player.length:
                    length = self.game.player.length
                    steps_without_food = 0

                if steps_without_food >= 1000:
                    break

            # keep track of important metrics
            self.score.append(self.game.player.length)
            self.survived.append(self.game.survived)

    def run_episode(self, episode):
        self._load_model(episode)
        self.game = Game()
        current_state = self.game.get_state()

        done = False
        while not done:
            for event in pygame.event.get():
                if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                    pygame.quit()
                    sys.exit()

            # choose action and take it
            action = self.get_action(current_state)
            current_state, reward, done = self.game.step(action)

            CLOCK.tick(FPS)

    def _load_model(self, episode):
        filename = f'pickle/snake_model_{episode}.pickle'

        with open(filename, 'rb') as file:
            self.table = pickle.load(file)

        self.epsilon = max(self.epsilon * self.epsilon_discount ** episode, self.min_epsilon)
