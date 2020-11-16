from enum import Enum
from typing import List

import pygame
from pygame.locals import *


class Events(Enum):
    QUIT = 1,
    RESTART = 2,
    LAUNCH = 3,
    PRESS_LEFT = 4,
    RELEASE_LEFT = 5,
    PRESS_RIGHT = 6,
    RELEASE_RIGHT = 7


class Listener:

    def yield_events(self) -> List[Events]:
        pass


class KeyBoardListener(Listener):

    def yield_events(self) -> List[Events]:
        events = []
        for event in pygame.event.get():
            if event.type == QUIT:
                events.append(Events.QUIT)
            if event.type == KEYDOWN:
                if event.key == K_F5:
                    events.append(Events.RESTART)

            if event.type == KEYDOWN:
                if event.key == K_z:
                    events.append(Events.PRESS_LEFT)
                if event.key == K_m:
                    events.append(Events.PRESS_RIGHT)
                if event.key == K_SPACE:
                    events.append(Events.LAUNCH)

            if event.type == KEYUP:
                if event.key == K_z:
                    events.append(Events.RELEASE_LEFT)
                if event.key == K_m:
                    events.append(Events.RELEASE_RIGHT)

        return events

