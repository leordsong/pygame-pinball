import numpy as np
import math

from engine.shapes import Circle, ConvexPolygon
from engine import Transform, Material
from engine.Entity import Entity


class Flipper(Entity):

    def __init__(self, center: np.ndarray, head: np.ndarray, angle: float, material: Material, name="Flipper",
                 center_r: float = 12.0, head_r: float = 7.0):
        super().__init__(Circle(center_r, Transform(center)), material, 100, name=name)
        self.angle = angle
        self.original_head = head
        self.rotated_head = self._rotate(center, head, angle)

        self.head_shape = Circle(head_r, Transform(self.original_head))
        self.original_points = self._calculate_points(center, center_r, self.original_head, head_r)
        self.rotated_points = self._calculate_points(center, center_r, self.rotated_head, head_r)
        self.body_shape = ConvexPolygon(self.original_points, Transform(center))

    def rotate(self, active):
        if active:
            self.head_shape.transform.position = self.rotated_head
            self.body_shape.points = self.rotated_points
        else:
            self.head_shape.transform.position = self.original_head
            self.body_shape.points = self.original_points

    def reset(self):
        self.rotate(False)

    @staticmethod
    def _calculate_points(center, center_r, head, head_r):
        result = []
        length = math.sqrt((head[0] - center[0]) ** 2 + (head[1] - center[1]) ** 2)
        sin_angle = (head[1] - center[1]) / length
        cos_angle = (head[0] - center[0]) / length
        result.append([center[0] - sin_angle * center_r, center[1] + cos_angle * center_r])
        result.append([center[0] + sin_angle * center_r, center[1] - cos_angle * center_r])
        result.append([head[0] + sin_angle * head_r, head[1] - cos_angle * head_r])
        result.append([head[0] - sin_angle * head_r, head[1] + cos_angle * head_r])
        return np.array(result)

    @staticmethod
    def _rotate(origin, point, angle):
        """
        Rotate a point counterclockwise by a given angle around a given origin.

        The angle should be given in radians.
        """
        ox, oy = origin
        px, py = point

        qx = ox + math.cos(angle) * (px - ox) - math.sin(angle) * (py - oy)
        qy = oy + math.sin(angle) * (px - ox) + math.cos(angle) * (py - oy)
        return [qx, qy]

    def draw(self, screen):
        self.head_shape.render(screen, self.material)
        self.body_shape.render(screen, self.material)
        self.shape.render(screen, self.material)
