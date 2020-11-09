import numpy as np
import pygame
import sys
from pygame.locals import *
from pygame.color import THECOLORS
import math

from engine import Entity, Transform
from engine.Material import Material
from engine.shapes import Rectangle, ConvexPolygon
from game.Ball import Ball
from game.Bumper import Bumper
from game.Flipper import Flipper

# Initialize program
from game.PhyscisEngine import get_contacts

pygame.init()

# Assign FPS a value
FPS = 60
FramePerSec = pygame.time.Clock()

# Create a window
WINDOW_TITLE = 'Pinball'
WINDOW_WIDTH = 300
WINDOW_HEIGHT = 500
DISPLAYSURF = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption(WINDOW_TITLE)

# Create Sprites
wall_material = Material(THECOLORS['black'], restitution=0.8)
walls = [
    Entity(Transform(np.array([0, 0]), 10), Rectangle(WINDOW_WIDTH - 40, 5), wall_material, "UpperWall"),
    Entity(Transform(np.array([0, 0]), 10), Rectangle(5, WINDOW_HEIGHT), wall_material, "LeftWall"),
    Entity(Transform(np.array([WINDOW_WIDTH - 40, 80]), 10), Rectangle(5, WINDOW_HEIGHT), wall_material, "MidWall"),
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
]

bumper_material = Material(THECOLORS['red'], restitution=0.9)
bumpers = [
    Bumper(np.array([30, 60]), material=bumper_material, name="Bumper1"),
    Bumper(np.array([105, 145]), material=bumper_material, name="Bumper2"),
    Bumper(np.array([165, 130]), material=bumper_material, name="Bumper3"),
]

flipper_material = Material(THECOLORS['red'], restitution=0.6)
left_flipper = Flipper(np.array([52, WINDOW_HEIGHT - 55]), np.array([102, WINDOW_HEIGHT - 25]), -math.pi / 4,
                       flipper_material, 'LeftFlipper')
right_flipper = Flipper(np.array([WINDOW_WIDTH - 90, WINDOW_HEIGHT - 55]),
                        np.array([WINDOW_WIDTH - 140, WINDOW_HEIGHT - 25]), math.pi / 4,
                        flipper_material, 'RightFlipper')

plunger = Entity(Transform(np.array([WINDOW_WIDTH - 25, WINDOW_HEIGHT - 40]), 10), Rectangle(10, 60), wall_material,
                 "Plunger")

static_group = walls + bumpers + [left_flipper, right_flipper, plunger]
ball = Ball(np.array([280, 450]), 10, Material(THECOLORS['green']))

# Create fonts
text_font = pygame.font.Font('freesansbold.ttf', 13)

# Beginning Game Loop
last_time = None
while True:

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:
            if event.key == K_z:
                left_flipper.rotate(True)
            if event.key == K_m:
                right_flipper.rotate(True)
            if event.key == K_SPACE:
                ball.launch()

        if event.type == KEYUP:
            if event.key == K_z:
                left_flipper.rotate(False)
            if event.key == K_m:
                right_flipper.rotate(False)

    t = pygame.time.get_ticks()
    delta_time = 0 if last_time is None else (t - last_time) / 1000
    last_time = t

    # first update
    for w in static_group:
        w.update(delta_time)
    ball.update(delta_time)

    # Check contacts
    contacts = get_contacts(ball, static_group)
    for contact in contacts:
        contact.resolve()

    # Render
    DISPLAYSURF.fill(THECOLORS['cadetblue1'])
    for w in static_group:
        w.draw(DISPLAYSURF)
    ball.draw(DISPLAYSURF)
    # Display Scores
    scores = 0
    scoreText = str(scores)
    score = text_font.render(scoreText, True, THECOLORS['black'])
    DISPLAYSURF.blit(score, (15, 10))

    pygame.display.update()
    FramePerSec.tick(FPS)
