import numpy as np
import math

import pygame

from engine.shapes import Circle, ConvexPolygon
from engine import Transform, Material
from engine.Entity import Entity
from utils import is_2d_array


class Flipper(Entity):

    def __init__(self, center: np.ndarray, head: np.ndarray, angle: float, material: Material, name="Flipper",
                 center_r: float = 12.0, head_r: float = 7.0, left=True):
        super().__init__(Circle(center_r, Transform(center)), material, 100, name=name)
        assert type(angle) is float
        is_2d_array(head)
        rotated_head = self._rotate(center, head, angle)
        self.original_head = Circle(head_r, Transform(head))
        self.rotated_head = Circle(head_r, Transform(rotated_head))

        original_points = self._calculate_points(center, center_r, head, head_r)
        rotated_points = self._calculate_points(center, center_r, rotated_head, head_r)
        self.original_body = ConvexPolygon(original_points, Transform(center))
        self.rotated_body = ConvexPolygon(rotated_points, Transform(center))

        points = np.array([rotated_points[0], original_points[1], rotated_points[2], original_points[3]]) if left \
            else np.array([original_points[0], rotated_points[1], original_points[2], rotated_points[3]])
        self.whole_body = ConvexPolygon(points, Transform(center))

        self.state = False
        self.prev_state = 0

    def rotate(self, active: bool):
        if not self.state:
            self.prev_state = pygame.time.get_ticks()
        self.state = active

    def reset(self):
        self.rotate(False)

    def is_active(self):
        active = pygame.time.get_ticks() - self.prev_state < 200
        if active:
            self.material.restitution = 1.5
        else:
            self.material.restitution = 0.9

    def collide_ball(self, ball) -> bool:
        if self.is_active():
            return ball.shape.collide(self.whole_body) or ball.shape.collide(self.rotated_head) \
                   or ball.shape.collide(self.shape)
        elif self.state:
                return ball.shape.collide(self.rotated_body) or ball.shape.collide(self.rotated_head) \
                       or ball.shape.collide(self.shape)
        else:
            return ball.shape.collide(self.original_body) or ball.shape.collide(self.original_head) \
                   or ball.shape.collide(self.shape)

    def get_contact_normal_ball(self, ball) -> bool:
        if self.is_active():
            if ball.shape.collide(self.rotated_head):
                return ball.shape.get_normal(self.rotated_head)
            if ball.shape.collide(self.shape):
                return ball.shape.get_normal(self.shape)
            elif ball.shape.collide(self.whole_body):
                return ball.shape.get_normal(self.whole_body)
        elif self.state:
            if ball.shape.collide(self.rotated_head):
                return ball.shape.get_normal(self.rotated_head)
            if ball.shape.collide(self.shape):
                return ball.shape.get_normal(self.shape)
            elif ball.shape.collide(self.whole_body):
                return ball.shape.get_normal(self.rotated_body)
        else:
            if ball.shape.collide(self.original_head):
                return ball.shape.get_normal(self.rotated_head)
            if ball.shape.collide(self.shape):
                return ball.shape.get_normal(self.shape)
            elif ball.shape.collide(self.original_body):
                return ball.shape.get_normal(self.rotated_body)

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
    def _rotate(origin: np.ndarray, point: np.ndarray, angle: float) -> np.ndarray:
        """
        Rotate a point counterclockwise by a given angle around a given origin.

        The angle should be given in radians.
        """
        p: np.ndarray = point - origin
        qx = math.cos(angle) * p[0] - math.sin(angle) * p[1]
        qy = math.sin(angle) * p[0] + math.cos(angle) * p[1]
        return origin + np.array([qx, qy])

    def draw(self, screen):
        if self.state:
            self.rotated_head.render(screen, self.material)
            self.rotated_body.render(screen, self.material)
        else:
            self.original_head.render(screen, self.material)
            self.original_body.render(screen, self.material)
        self.shape.render(screen, self.material)
