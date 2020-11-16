import numpy as np
from pygame.color import THECOLORS
import math

from engine import Entity, Transform, Material
from engine.shapes import Rectangle, ConvexPolygon
from game.Ball import Ball
from game.Bumper import Bumper
from game.Flipper import Flipper

# Initialize program
from game.Game import Game
from game.Listener import KeyBoardListener
from game.Valve import Valve

# Create a window
WINDOW_TITLE = 'Pinball'
WINDOW_WIDTH = 300
WINDOW_HEIGHT = 500

# Create Sprites
wall_material = Material(THECOLORS['black'], restitution=1)
walls = [
    Entity(Transform(np.array([0, 0]), 10), Rectangle(WINDOW_WIDTH - 40, 5), wall_material, "UpperWall"),
    Entity(Transform(np.array([0, 0]), 10), Rectangle(5, WINDOW_HEIGHT), wall_material, "LeftWall"),
    Entity(Transform(np.array([WINDOW_WIDTH - 5, 40]), 10), Rectangle(5, WINDOW_HEIGHT), wall_material, "RightWall"),
    Entity(Transform(np.array([WINDOW_WIDTH - 50, 0]), 100),
           ConvexPolygon(np.array([[WINDOW_WIDTH - 100, 0], [WINDOW_WIDTH, 0], [WINDOW_WIDTH, 50]])),
           wall_material, "TopRight"),
    Entity(Transform(np.array([5, WINDOW_HEIGHT - 69]), 10),
           ConvexPolygon(np.array([[5, WINDOW_HEIGHT - 69], [5, WINDOW_HEIGHT - 97],
                                   [57.91117863822124, 434.5569177391425], [46.08882136177876, 455.4430822608575]])),
           wall_material, "LeftArm"),
    Entity(Transform(np.array([WINDOW_WIDTH - 40, WINDOW_HEIGHT - 97]), 10),
           ConvexPolygon(np.array([[WINDOW_WIDTH - 40, WINDOW_HEIGHT - 97], [WINDOW_WIDTH - 40, WINDOW_HEIGHT - 69],
                                   [215.91117863822123, 455.4430822608575], [204.08882136177877, 434.5569177391425]])),
           wall_material, "RightArm"),
    Entity(Transform(np.array([WINDOW_WIDTH - 25, WINDOW_HEIGHT - 40]), 10), Rectangle(10, 60), wall_material,
           "Plunger")
]
middle_wall = Valve(Rectangle(5, WINDOW_HEIGHT - 100, np.array([WINDOW_WIDTH - 40, 100])),
                    Rectangle(5, WINDOW_HEIGHT, np.array([WINDOW_WIDTH - 40, 0])), wall_material, "MiddleWall")

bumper_material = Material(THECOLORS['red'], restitution=1.2)
bumpers = [
    Bumper(np.array([30, 60]), material=bumper_material, name="Bumper1"),
    Bumper(np.array([105, 145]), material=bumper_material, name="Bumper2"),
    Bumper(np.array([165, 130]), r=20, material=bumper_material, name="Bumper3"),
]

flipper_material = Material(THECOLORS['red'], restitution=0.6)
left_flipper = Flipper(np.array([52, WINDOW_HEIGHT - 55]), np.array([102, WINDOW_HEIGHT - 25]), -math.pi / 4,
                       flipper_material, 'LeftFlipper')
right_flipper = Flipper(np.array([WINDOW_WIDTH - 90, WINDOW_HEIGHT - 55]),
                        np.array([WINDOW_WIDTH - 140, WINDOW_HEIGHT - 25]), math.pi / 4,
                        flipper_material, 'RightFlipper')

ball = Ball(np.array([280, 450]), 14, Material(THECOLORS['green']))

# Start Game
game = Game("Pinball", WINDOW_WIDTH, WINDOW_HEIGHT, ball, left_flipper, right_flipper, middle_wall, walls + bumpers)
game.run(KeyBoardListener())
