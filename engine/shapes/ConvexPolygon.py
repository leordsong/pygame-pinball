import numpy as np
from pygame import gfxdraw

from engine.shapes.Shape import Shape


class ConvexPolygon(Shape):

    def __init__(self, points: np.array, position: np.ndarray = None):
        super().__init__(position)
        self.points = points

    def draw(self, ctx, material):
        gfxdraw.filled_polygon(ctx, self.points, material.color)
        gfxdraw.aapolygon(ctx, self.points, material.color)
