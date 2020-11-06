import pygame
from config import COLORS
from objects.Circle import Circle


class Bumper(Circle):

    def __init__(self, x, y, r=10, points=1, color=COLORS['ORANGE'], img=None, name="bumper"):
        super().__init__(x+r, y+r, r, color, [0, 0], name)
        self.points = points
        self.img = img

    def draw(self, ctx):
        if self.img is not None:
            ctx.blit(self.img, (self.x - self.r, self.y - self.r))
        else:
            pygame.draw.circle(ctx, self.color, (self.x, self.y), self.r)
