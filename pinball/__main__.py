import sys
from typing import List

import numpy as np
import pygame
from pygame.locals import *
from pygame.color import THECOLORS
import math

from engine import Game, Material, Transform
from engine import Entity, get_contacts
from engine.shapes import Rectangle, ConvexPolygon
from pinball.Valve import Valve
from pinball.Ball import Ball
from pinball.Bumper import Bumper
from pinball.Flipper import Flipper
from pinball.Wall import Wall


class PinballGame(Game):
    game_over = False
    last_game_over = False
    launched = False
    ball: Ball = None
    left_flipper: Flipper = None
    right_flipper: Flipper = None
    valve: Valve = None
    text_font = None
    text_font2 = None
    walls: List[Entity] = []
    bumpers: List[Bumper] = []

    def __init__(self):
        super().__init__('Pinball', 300, 500, THECOLORS['white'])

    def init(self):
        self.text_font = pygame.font.Font('freesansbold.ttf', 13)
        self.text_font2 = pygame.font.Font('freesansbold.ttf', 20)

        self.ball = Ball(np.array([280, 450]), 14.0, Material(THECOLORS['green']))

        wall_material = Material(THECOLORS['black'])
        wall_width = 5.0
        self.walls = [
            Wall(np.array([0, 0]), float(self.width), wall_width, wall_material, "UpperWall"),
            Wall(np.array([0, 0]), wall_width, float(self.height), wall_material, "LeftWall"),
            Wall(np.array([self.width - wall_width, 0]), wall_width, float(self.height), wall_material, "RightWall"),
            Wall(np.array([self.width - 25.0, self.height - 35.0]), 10.0, 35.0, wall_material, "Plunger"),
            Entity(ConvexPolygon(np.array([[self.width - 100, 0], [self.width, 0], [self.width, 50]]),
                                 Transform(np.array([self.width, self.height]))),
                   wall_material, 100, name="TopRight"),
            Entity(ConvexPolygon(np.array([[5, self.height - 69], [5, self.height - 97],
                                           [57.91117863822124, 434.5569177391425],
                                           [46.08882136177876, 455.4430822608575]]),
                                 Transform(np.array([5, self.height - 69]))),
                   wall_material, 100, name="LeftArm"),
            Entity(ConvexPolygon(np.array([[self.width - 40, self.height - 97], [self.width - 40, self.height - 69],
                                           [215.91117863822123, 455.4430822608575],
                                           [204.08882136177877, 434.5569177391425]]),
                                 Transform(np.array([self.width - 40, self.height - 97]))),
                   wall_material, 100, name="RightArm"),
        ]

        self.valve = Valve(Rectangle(5.0, self.height - 100.0, Transform(np.array([self.width - 40, 100]))),
                           Rectangle(5.0, float(self.height), Transform(np.array([self.width - 40, 0]))), wall_material,
                           "MiddleWall")

        bumper_material = Material(THECOLORS['red'], restitution=1.2)
        self.bumpers = [
            Bumper(np.array([50, 60]), material=bumper_material, name="Bumper1"),
            Bumper(np.array([105, 345]), material=bumper_material, name="Bumper2"),
            Bumper(np.array([165, 200]), r=20.0, material=bumper_material, name="Bumper3"),
        ]

        flipper_material = Material(THECOLORS['red'])
        self.left_flipper = Flipper(np.array([52, self.height - 55]), np.array([102, self.height - 25]), -math.pi / 4,
                                    flipper_material, 'LeftFlipper')
        self.right_flipper = Flipper(np.array([self.width - 90, self.height - 55]),
                                     np.array([self.width - 140, self.height - 25]), math.pi / 4,
                                     flipper_material, 'RightFlipper', left=False)

    def handle_actions(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_F5:
                    self.reset()

            if event.type == KEYDOWN:
                if event.key == K_z:
                    self.left_flipper.rotate(True)
                if event.key == K_m:
                    self.right_flipper.rotate(True)
                if event.key == K_SPACE:
                    self.ball.launch()

            if event.type == KEYUP:
                if event.key == K_z:
                    self.left_flipper.rotate(False)
                if event.key == K_m:
                    self.right_flipper.rotate(False)

    def step(self, delta_time):
        if self.game_over:
            self.last_game_over = True
        self.ball.update(delta_time)

        static_group = [self.left_flipper, self.right_flipper, self.valve] + self.walls + self.bumpers
        # Check contacts
        contacts = get_contacts(self.ball, static_group)
        if len(contacts) > 0:
            self.ball.revert()
        for contact in contacts:
            contact.resolve(delta_time)
        if len(contacts) > 0:
            self.ball.update(delta_time / 2)

        if self.ball.transform.position[1] >= self.height:
            self.game_over = True
        if not self.launched and self.ball.transform.position[0] <= (self.width - 40 - self.ball.shape.r):
            self.launched = True
            self.valve.trigger()
        for contact in contacts:
            if isinstance(contact.body_b, Bumper):
                self.score += contact.body_b.points

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

        score_text = self.text_font.render(str(int(self.score)), True, THECOLORS['black'])
        self.screen.blit(score_text, (15, 10))
        if self.game_over:
            game_over_text = self.text_font2.render("Game Over", True, THECOLORS['black'])
            self.screen.blit(game_over_text, (self.width / 2 - 60, self.height / 2))

    def is_game_over(self) -> bool:
        return self.game_over

    def needs_update_frame(self):
        return not (self.game_over and self.last_game_over)

    def reset(self):
        self.last_time = 0
        self.score = 0
        self.game_over = False
        self.last_game_over = False
        self.launched = False
        self.ball.reset()
        self.left_flipper.reset()
        self.right_flipper.reset()
        self.valve.reset()


if __name__ == '__main__':
    game = PinballGame()
    game.run()
