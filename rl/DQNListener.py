from typing import List

from game.Listener import Listener, Events
from rl.DQNAgent import DQNAgent


class DQNListener(Listener):

    prev_action = [0, 0, 0]
    action = [0, 0, 0]  # do nothing

    def __init__(self, episodes):
        self.agent = DQNAgent()
        self.agent.network()

    def yield_events(self) -> List[Events]:
        events = []

        return events