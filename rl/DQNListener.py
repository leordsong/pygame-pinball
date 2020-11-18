from typing import List

import numpy as np

from engine.InputEngine import Listener
from pinball.Listener import Events
from rl.DQNAgent import DQNAgent


class DQNListener(Listener):

    prev_action = [0, 0, 0]
    action = [0, 0, 0]  # do nothing

    counters = 0
    frames = 0
    batch_size = 500

    def __init__(self, agent: DQNAgent, skip: int):
        self.agent = agent
        self.skip = skip

    def yield_events(self, game) -> List[str]:
        events = []
        if self.counters > self.agent.episodes:
            events.append(Events.QUIT.value)
            return events
        if game.is_game_over():
            self.counters = self.counters + 1
            self.frames = 0
            events.append(Events.RESTART.value)
            self.agent.replay_new(self.agent.memory)
            return events
        if self.frames < self.skip:
            self.action = np.array([0, 0, 0])
        else:
            prediction = self.agent.predict(game.get_grey_screen())
            self.action = np.argmax(prediction[0])
        if self.action[0] == 1:
            if self.action[0] == 0:
                events.append(Events.PRESS_LEFT)
        if self.action[0] == 0:
            if self.action[0] == 1:
                events.append(Events.RELEASE_LEFT)
        if self.action[1] == 1:
            if self.action[1] == 0:
                events.append(Events.PRESS_RIGHT)
        if self.action[1] == 0:
            if self.action[1] == 1:
                events.append(Events.RELEASE_RIGHT)
        if self.action[2] == 0:
            events.append(Events.LAUNCH)
        self.prev_action = self.action
        self.frames = self.frames + 1
        return events
