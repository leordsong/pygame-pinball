from enum import Enum
from typing import List

import pygame
from pygame.locals import *

from engine.InputEngine import Listener


class Events(Enum):
    QUIT = "QUIt",
    RESTART = "RESTART",
    LAUNCH = "LAUNCH",
    PRESS_LEFT = "PRESS_LEFT",
    RELEASE_LEFT = "RELEASE_LEFT",
    PRESS_RIGHT = "PRESS_RIGHT",
    RELEASE_RIGHT = "RELEASE_RIGHT"


class KeyBoardListener(Listener):

    def yield_events(self) -> List[str]:
        events = []
        for event in pygame.event.get():
            if event.type == QUIT:
                events.append(Events.QUIT.value)
            if event.type == KEYDOWN:
                if event.key == K_F5:
                    events.append(Events.RESTART.value)

            if event.type == KEYDOWN:
                if event.key == K_z:
                    events.append(Events.PRESS_LEFT.value)
                if event.key == K_m:
                    events.append(Events.PRESS_RIGHT.value)
                if event.key == K_SPACE:
                    events.append(Events.LAUNCH.value)

            if event.type == KEYUP:
                if event.key == K_z:
                    events.append(Events.RELEASE_LEFT.value)
                if event.key == K_m:
                    events.append(Events.RELEASE_RIGHT.value)

        return events
