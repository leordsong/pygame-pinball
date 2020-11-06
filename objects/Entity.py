import pygame


class Entity(pygame.sprite.Sprite):

    def __init__(self, x, y, color, spd, name="none"):
        super().__init__()
        self.x = x
        self.y = y
        self.color = color
        self.spd = spd
        self.name = name

    def draw(self, ctx):
        pass
