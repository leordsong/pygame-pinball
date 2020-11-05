import pygame
import sys
from pygame.locals import *
from objects.Rect import Rect

# Initialize program
pygame.init()

# Assign FPS a value
FPS = 60
FramePerSec = pygame.time.Clock()

# Setting up color objects
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
gameW = 400
gameH = 600

# Setup a 400x600 pixel display with caption
DISPLAYSURF = pygame.display.set_mode((gameW, gameH))
DISPLAYSURF.fill(WHITE)
pygame.display.set_caption("Pinball game")

# Creating Objects
walls = [
    Rect(0, 0, gameW, 10, BLACK, [0, 0]),
    Rect(0, 0, 20, gameH, BLACK, [0, 0]),
    Rect(gameW - 40, 0, 40, gameH, BLACK, [0, 0])
]


font = pygame.font.Font('freesansbold.ttf', 13)


# Beginning Game Loop
while True:
    DISPLAYSURF.fill(WHITE)
    # Add objects
    for w in walls:
        w.go(DISPLAYSURF)
    # Display FPS
    fpsTEXT = str(round(FramePerSec.get_fps(), 1))
    fps = font.render(fpsTEXT, True, BLACK)
    DISPLAYSURF.blit(fps, (25, 10))

    pygame.display.update()

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    FramePerSec.tick(FPS)
