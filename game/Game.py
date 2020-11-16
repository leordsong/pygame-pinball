import string
import sys
from typing import List

import pygame
from pygame.color import THECOLORS

from engine import Entity, get_contacts
from game.Ball import Ball
from game.Bumper import Bumper
from game.Flipper import Flipper
from game.Listener import Listener, Events
from game.Valve import Valve


class Game:
    last_time: int = 0
    scores = 0
    game_over = False
    launched = False
    FPS = 60

    def __init__(self, name: string, width: int, height: int, ball: Ball, left_flipper: Flipper,
                 right_flipper: Flipper, valve: Valve, walls: List[Entity]):
        pygame.init()
        self.name = name
        self.width = width
        self.height = height
        self.ball = ball
        self.left_flipper = left_flipper
        self.right_flipper = right_flipper
        self.valve = valve
        self.walls = walls
        self.text_font = pygame.font.Font('freesansbold.ttf', 13)
        self.text_font2 = pygame.font.Font('freesansbold.ttf', 20)
        self.initialize()

    def initialize(self):
        self.last_time = 0
        self.scores = 0
        self.game_over = False
        self.launched = False
        self.ball.initialize()
        self.left_flipper.initialize()
        self.right_flipper.initialize()
        self.valve.initialize()
        for w in self.walls:
            w.initialize()

    def run(self, listener: Listener):

        DISPLAYSURF = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption(self.name)
        FramePerSec = pygame.time.Clock()

        while True:
            for event in listener.yield_events():
                event: Events
                if event == Events.QUIT:
                    pygame.quit()
                    sys.exit()
                if event == Events.RESTART:
                    self.initialize()
                if not self.game_over:
                    if event == Events.PRESS_LEFT:
                        self.left_flipper.rotate(True)
                    if event == Events.RELEASE_LEFT:
                        self.left_flipper.rotate(False)
                    if event == Events.PRESS_RIGHT:
                        self.right_flipper.rotate(True)
                    if event == Events.RELEASE_RIGHT:
                        self.right_flipper.rotate(False)
                    if event == Events.LAUNCH:
                        self.ball.launch()

            static_group = [self.left_flipper, self.right_flipper, self.valve] + self.walls

            if not self.game_over:
                t = pygame.time.get_ticks()
                delta_time = 0 if self.last_time is 0 else (t - self.last_time) / 1000
                self.last_time = t

                # first update
                for w in static_group:
                    w.update(delta_time)
                self.ball.update(delta_time)

                # Check contacts
                contacts = get_contacts(self.ball, static_group)
                if len(contacts) > 0:
                    self.ball.revert()
                for contact in contacts:
                    contact.resolve(delta_time)
                if len(contacts) > 0:
                    self.ball.update(delta_time / 2)

                # Add points
                for contact in contacts:
                    if isinstance(contact.body_b, Bumper):
                        self.scores += contact.body_b.points

                if self.ball.transform.position[1] >= self.height:
                    self.game_over = True
                if not self.launched and self.ball.transform.position[0] <= (self.width - 40 - self.ball.shape.r):
                    self.launched = True
                    self.valve.trigger()

            # Render
            DISPLAYSURF.fill(THECOLORS['cadetblue1'])
            for w in static_group:
                w.draw(DISPLAYSURF)
            self.ball.draw(DISPLAYSURF)
            # Display Scores
            score_text = str(self.scores)
            score = self.text_font.render(score_text, True, THECOLORS['black'])
            DISPLAYSURF.blit(score, (15, 10))
            if self.game_over:
                game_over_text = self.text_font2.render("Game Over", True, THECOLORS['black'])
                DISPLAYSURF.blit(game_over_text, (self.width / 2 - 60, self.height / 2))

            # imgdata = pygame.surfarray.array3d(DISPLAYSURF)

            pygame.display.update()
            FramePerSec.tick(self.FPS)
