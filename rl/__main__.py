import sys
from random import randint

import numpy as np
import pygame
import pandas as pd
from os.path import join

from pinball.__main__ import PinballGame
from rl.DQNAgent import DQNAgent


class RLPinballGame(PinballGame):
    prev_action = 0
    action = 0  # do nothing

    counters = 0
    frames = 0
    batch_size = 500
    skip = 21
    train = False
    last_state = None
    data = pd.DataFrame(columns=['episode', 'score'])

    def __init__(self, agent: DQNAgent, train: bool, display: bool, episodes: int, batch_size: int,
                 weight_path: str = None):
        super().__init__()
        self.agent = agent
        self.train = train
        self.display = display
        self.episodes = episodes
        self.batch_size = batch_size
        self.weight_path = weight_path

    def handle_actions(self):
        events = []
        if self.counters > self.episodes:
            if self.train:
                self.agent.save_weights(self.weight_path)
                if self.weight_path is not None:
                    self.data.to_csv(join(self.weight_path, 'result.csv'))
            pygame.quit()
            sys.exit()
        if self.is_game_over():
            self.reset()

        if self.frames == 21:
            self.ball.launch()
        if self.frames < self.skip:
            self.action = 0
            if self.last_state is not None:
                self.agent.predict(self.last_state)
        else:
            self.action = self.make_action()
            self.left_flipper.rotate(self.action == 1)
            self.right_flipper.rotate(self.action == 2)
        self.prev_action = self.action
        return events

    def make_action(self):
        self.agent.adjust_epsilon(self.counters)
        if np.random.rand() < self.agent.epsilon:
            return randint(0, 2)
        else:
            prediction = self.agent.predict(self.last_state)
            return np.argmax(prediction[0])

    def needs_update_frame(self):
        return self.display

    def render(self):
        self.screen.fill(self.background)
        self.ball.draw(self.screen)
        self.valve.draw(self.screen)
        for w in self.walls:
            w.draw(self.screen)
        for w in self.bumpers:
            w.draw(self.screen)
        self.left_flipper.draw(self.screen)
        self.right_flipper.draw(self.screen)

    def reset(self):
        super().reset()
        self.counters = self.counters + 1
        self.frames = 0

    def run(self):
        self._setup()
        self.init()
        self.agent.network(self.width, self.height, 3, self.weight_path)
        self.agent.model.summary()
        while True:
            self.handle_actions()
            self.update()
            self.render()
            self.agent.set_reward(self.score, self.is_game_over())

            # remember each state
            state = None
            if self.frames >= self.skip and self.train:
                state = self.get_grey_screen()
                if self.frames % 10 == 0:
                    self.agent.remember(self.last_state, self.action, self.agent.reward, state, self.is_game_over())
                    self.agent.train_short_memory(self.last_state, self.action, self.agent.reward, state,
                                                  self.is_game_over())
                self.last_state = state
            self.last_state = self.get_grey_screen() if state is None else state

            if self.needs_update_frame():
                self.update_frame()
            self.frames = self.frames + 1
            if self.is_game_over():
                print("Episode: ", self.counters)
                self.agent.train(self.agent.memory, self.batch_size)
                self.data = self.data.append({'episode': self.counters, 'score': self.score}, ignore_index=True)
            self.tick()


if __name__ == '__main__':
    agent1 = DQNAgent("dqn")
    game = RLPinballGame(agent1, True, True, 20, 500, './weights')
    game.run()
