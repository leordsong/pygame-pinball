import numpy as np
import pygame

from engine import Material
from engine.shapes.Shape import Shape


class Rectangle(Shape):

    def __init__(self, width, height, position: np.ndarray = None):
        super().__init__(position)
        self.width = width
        self.height = height

    def draw(self, ctx, material: Material):
        if material.image is not None:
            ctx.blit(material.image, self.position)
        else:
            pygame.draw.rect(ctx, material.color, (self.position[0], self.position[1], self.width, self.height))

    def get_points(self):
        x0 = self.position[0]
        x = x0 + self.width
        y0 = self.position[1]
        y = y0 + self.height
        return np.array([[x0, y0], [x, y0], [x, y], [x0, y]])
