import sys
from typing import List

import numpy as np
import pygame

from pinball.__main__ import PinballGame
from rl.DQNAgent import DQNAgent


class RLPinballGame(PinballGame):
    prev_action = [0, 0, 0]
    action = [0, 0, 0]  # do nothing

    counters = 0
    frames = 0
    batch_size = 500
    skip = 1
    train = False
    last_state = None

    def __init__(self, agent: DQNAgent):
        super().__init__()
        self.agent = agent

    def handle_actions(self, actions: List[str]):
        events = []
        if self.counters > self.agent.episodes:
            pygame.quit()
            sys.exit()
        if self.is_game_over():
            self.counters = self.counters + 1
            self.frames = 0
            self.reset()
            self.agent.replay_new(self.agent.memory)
            return
        if self.frames < self.skip:
            self.action = np.array([0, 0, 0])
        else:
            prediction = self.agent.predict(self.last_state)
            self.action = np.argmax(prediction[0])
            self.left_flipper.rotate(self.action[0] == 1)
            self.right_flipper.rotate(self.action[1] == 1)
            if self.action[2] == 1:
                self.ball.launch()
        self.prev_action = self.action
        self.frames = self.frames + 1
        return events

    def run(self):
        self._setup()
        self.init()
        while True:
            t = pygame.time.get_ticks()
            delta_time = 0.0 if self.last_time is 0 else (t - self.last_time) / 1000
            self.last_time = t
            self.handle_actions(self.listener.yield_events(self))
            self.step(delta_time)
            self.render()
            self.agent.set_reward(self.score, self.is_game_over())
            if self.train:
                state = self.get_grey_screen()
                self.agent.train_short_memory(state, self.action, self.score, self.last_state,
                                              self.is_game_over())
                self.agent.remember(state, self.action, self.score, self.last_state, self.is_game_over())
                self.last_state = state
            if self.needs_update_frame():
                self.update_frame()
            self.tick()
