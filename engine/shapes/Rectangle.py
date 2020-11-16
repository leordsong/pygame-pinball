import numpy as np
import pygame

from engine import Material
from engine.shapes.ConvexPolygon import ConvexPolygon


class Rectangle(ConvexPolygon):

    def __init__(self, width, height, position: np.ndarray = np.array([0, 0])):
        super().__init__(self._get_points(position, width, height), position)
        self.width = width
        self.height = height

    def update_position(self, position: np.array):
        self.position = position
        self.points = self._get_points(position, self.width, self.height)

    def draw(self, ctx, material: Material):
        if material.image is not None:
            ctx.blit(material.image, self.position)
        else:
            pygame.draw.rect(ctx, material.color, (self.position[0], self.position[1], self.width, self.height))

    @staticmethod
    def _get_points(position, width, height):
        x0 = position[0]
        x = x0 + width
        y0 = position[1]
        y = y0 + height
        return np.array([[x0, y0], [x, y0], [x, y], [x0, y]])
