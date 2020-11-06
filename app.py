import pygame
import sys
from pygame.locals import *
import math

from objects.Ball import Ball
from objects.Bumper import Bumper
from objects.Flipper import Flipper
from objects.Ploygon import Polygon
from objects.Rect import Rect
from config import WINDOW_TITLE, WINDOW_WIDTH, WINDOW_HEIGHT, COLORS, FONT

# Initialize program
pygame.init()

# Assign FPS a value
FPS = 60
FramePerSec = pygame.time.Clock()

# Create a window
DISPLAYSURF = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
DISPLAYSURF.fill(COLORS['WHITE'])
pygame.display.set_caption(WINDOW_TITLE)

# Create Sprites
walls = [
    Rect(0, 0, WINDOW_WIDTH - 40, 5, COLORS['BLACK'], [0, 0]),
    Rect(0, 0, 5, WINDOW_HEIGHT, COLORS['BLACK'], [0, 0]),
    Rect(WINDOW_WIDTH - 40, 80, 5, WINDOW_HEIGHT, COLORS['BLACK'], [0, 0]),
    Rect(WINDOW_WIDTH - 5, 40, 5, WINDOW_HEIGHT, COLORS['BLACK'], [0, 0]),
    Polygon([[WINDOW_WIDTH - 50, 0], [WINDOW_WIDTH, 0], [WINDOW_WIDTH, 50]], 0, COLORS['BLACK'], [0, 0]),

    Polygon([[5, WINDOW_HEIGHT - 80], [5, WINDOW_HEIGHT - 90], [52, WINDOW_HEIGHT - 60], [52, WINDOW_HEIGHT - 50]], 0,
            COLORS['BLACK'], [0, 0]),
    Polygon([[WINDOW_WIDTH - 40, WINDOW_HEIGHT - 90], [WINDOW_WIDTH - 40, WINDOW_HEIGHT - 80],
             [WINDOW_WIDTH - 90, WINDOW_HEIGHT - 50], [WINDOW_WIDTH - 90, WINDOW_HEIGHT - 60]],
            0, COLORS['BLACK'], [0, 0]),
]

bumpers = [
    Bumper(30, 60),
    Bumper(105, 145),
    Bumper(165, 130),
]

left_flipper = Flipper((52, WINDOW_HEIGHT - 55),
                       [[52, WINDOW_HEIGHT - 50], [52, WINDOW_HEIGHT - 60], [102, WINDOW_HEIGHT - 30],
                        [102, WINDOW_HEIGHT - 20]],
                       -math.pi / 4, COLORS['RED'], [0, 0])
right_flipper = Flipper((WINDOW_WIDTH - 90, WINDOW_HEIGHT - 55),
                        [[WINDOW_WIDTH - 90, WINDOW_HEIGHT - 60], [WINDOW_WIDTH - 90, WINDOW_HEIGHT - 50],
                         [WINDOW_WIDTH - 140, WINDOW_HEIGHT - 20],
                         [WINDOW_WIDTH - 140, WINDOW_HEIGHT - 30]],
                        math.pi / 4, COLORS['RED'], [0, 0])

plunger = Rect(WINDOW_WIDTH - 25, WINDOW_HEIGHT - 40, 10, 60, COLORS['ORANGE'], [0, 0])
ball = Ball(280, 450, 10, COLORS['GREEN'])

# Create fonts
text_font = pygame.font.Font(FONT, 13)

# Beginning Game Loop
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
        if event.type == KEYUP:
            if event.key == K_z:
                left_flipper.rotate(False)
            if event.key == K_m:
                right_flipper.rotate(False)

    DISPLAYSURF.fill(COLORS['WHITE'])
    # Display objects
    for w in walls:
        w.draw(DISPLAYSURF)
    for w in bumpers:
        w.draw(DISPLAYSURF)
    left_flipper.draw(DISPLAYSURF)
    right_flipper.draw(DISPLAYSURF)
    plunger.draw(DISPLAYSURF)
    ball.draw(DISPLAYSURF)
    # Display Scores
    scores = 0
    scoreText = str(scores)
    score = text_font.render(scoreText, True, COLORS['BLACK'])
    DISPLAYSURF.blit(score, (15, 10))

    pygame.display.update()
    FramePerSec.tick(FPS)
