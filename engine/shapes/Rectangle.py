import numpy as np
import pygame

from engine.Transform import Transform
from engine.Material import Material
from engine.shapes.ConvexPolygon import ConvexPolygon
from engine.utils import is_2d_array


class Rectangle(ConvexPolygon):

    def __init__(self, width: float, height: float, transform: Transform):
        super().__init__(self._get_points(transform.position, width, height), transform, "Rectangle")
        assert type(width) is float
        self.width = width
        assert type(height) is float
        self.height = height

    def update(self):
        self.points = self._get_points(self.transform.position, self.width, self.height)

    def render(self, ctx, material: Material):
        assert isinstance(material, Material)
        if material.image is not None:
            ctx.blit(material.image, self.transform.position)
        else:
            pygame.draw.rect(ctx, material.color,
                             [self.transform.position[0], self.transform.position[1], self.width, self.height])

    def is_point_in_shape(self, point: np.ndarray) -> bool:
        is_2d_array(point)
        vector = point - self.transform.position
        return 0 <= vector[0] <= self.width and 0 <= vector[1] <= self.height

    @staticmethod
    def _get_points(position: np.ndarray, width: float, height: float) -> np.ndarray:
        x0 = position[0]
        x = x0 + width
        y0 = position[1]
        y = y0 + height
        return np.array([[x0, y0], [x, y0], [x, y], [x0, y]])
