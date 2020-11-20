from typing import Tuple

import numpy as np
import pygame

from engine.utils import is_color_tuple


class Game:

    def __init__(self, name: str, width: int, height: int, background: Tuple[int, int, int, int]):
        assert type(name) is str
        self.name = name
        assert type(width) is int
        self.width = width
        assert type(height) is int
        self.height = height
        self.background = is_color_tuple(background)

        self.score = 0.0
        self.screen = None
        self.clock = None
        self.fps = 60
        self.last_time = 0

    def _setup(self):
        pygame.init()
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption(self.name)
        self.clock = pygame.time.Clock()

    def get_grey_screen(self):
        rgb = pygame.surfarray.array3d(self.screen).astype(np.float)
        return rgb / 255

    def init(self):
        raise NotImplementedError("This method needs to be implemented")

    def handle_actions(self):
        raise NotImplementedError("This method needs to be implemented")

    def update(self):
        t = pygame.time.get_ticks()
        delta_time = 0.0 if self.last_time is 0 else (t - self.last_time) / 1000
        self.last_time = t
        self.step(delta_time)

    def step(self, delta_time):
        raise NotImplementedError("This method needs to be implemented")

    def render(self):
        raise NotImplementedError("This method needs to be implemented")

    def needs_update_frame(self):
        raise NotImplementedError("This method needs to be implemented")

    @staticmethod
    def update_frame():
        pygame.display.update()

    def tick(self):
        return self.clock.tick(self.fps)

    def is_game_over(self) -> bool:
        raise NotImplementedError("This method needs to be implemented")

    def reset(self):
        raise NotImplementedError("This method needs to be implemented")

    def run(self):
        self._setup()
        self.init()
        while True:
            self.handle_actions()
            self.update()
            self.render()
            if self.needs_update_frame():
                self.update_frame()
            self.tick()
