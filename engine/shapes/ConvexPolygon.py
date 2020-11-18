from typing import Optional

import numpy as np
from pygame import gfxdraw

from engine import Material
from engine.Transform import Transform
from engine.shapes.Shape import Shape
from utils import is_polygon_array, is_2d_array


class ConvexPolygon(Shape):

    def __init__(self, points: np.ndarray, transform: Transform, name: Optional[str] = None):
        super().__init__(transform, "ConvexPolygon" if name is None else name)
        self.points = is_polygon_array(points)

    def render(self, ctx, material: Material):
        assert isinstance(material, Material)
        gfxdraw.filled_polygon(ctx, self.points, material.color)
        gfxdraw.aapolygon(ctx, self.points, material.color)

    def is_point_in_shape(self, point: np.ndarray) -> bool:
        is_2d_array(point)
        number_of_edges = self.points.shape[0]
        a = self.points[0]
        for i in range(number_of_edges - 2):
            b = self.points[i + 1]
            c = self.points[i + 2]
            if self._point_in_triangle(point, a, b, c):
                return True
        return False

    @staticmethod
    def _point_in_triangle(point: np.ndarray, a: np.ndarray, b: np.ndarray, c: np.ndarray):
        as_x = point[0] - a[0]
        as_y = point[1] - a[1]

        s_ab = (b[0] - a[0]) * as_y - (b[1] - a[1]) * as_x > 0

        if ((c[0] - a[0]) * as_y - (c[1] - a[1]) * as_x > 0) == s_ab:
            return False

        if ((c[0] - b[0]) * (point[1] - b[1]) - (c[1] - b[1]) * (point[0] - b[0]) > 0) != s_ab:
            return False

        return True
