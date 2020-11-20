import numpy as np
import math

import pygame

from engine.shapes import Circle, ConvexPolygon
from engine import Transform, Material
from engine.Entity import Entity


class Flipper(Entity):

    def __init__(self, center: np.ndarray, head_pos: np.ndarray, angle: float, material: Material, name="Flipper",
                 center_r: float = 12.0, head_r: float = 7.0):
        assert type(angle) is float

        self.head = Circle(head_r, Transform(head_pos))
        self.body = ConvexPolygon(self._calculate_points(center, center_r, head_pos, head_r), Transform(center))
        self.tail = Circle(center_r, Transform(center))
        super().__init__(self.tail, material, 100, name=name)

        self.angle = angle
        self.center = center
        self.head_position = head_pos
        self.state = False
        self.prev_time = 0
        self.step = 0
        self.max_step = 20

    def rotate(self, active: bool):
        if active != self.state:
            self.prev_time = pygame.time.get_ticks()
        self.state = active

    def reset(self):
        self.step = 0
        self.state = False
        self.prev_time = 0

    def collide_ball(self, ball) -> bool:
        if ball.shape.collide(self.head):
            self.shape = self.head
            self.material.restitution = 1.5 if self.state else 0.9
            return True
        elif ball.shape.collide(self.body):
            self.shape = self.body
            self.material.restitution = 1.2 if self.state else 0.9
            return True
        elif ball.shape.collide(self.tail):
            self.shape = self.tail
            self.material.restitution = 0.9
            return True
        return False

    def update(self, delta_time: float):
        if self.state:
            if self.step == self.max_step:
                return
            delta_time = pygame.time.get_ticks() - self.prev_time
            steps = int(delta_time / 10)
            self.step = self.step + steps
            if self.step > self.max_step:
                self.step = self.max_step
        else:
            if self.prev_time <= 0 or self.step == 0:
                return
            delta_time = pygame.time.get_ticks() - self.prev_time
            steps = int(delta_time / 10)
            self.step = self.step - steps
            if self.step < 0:
                self.step = 0

        angle = self.angle * self.step / self.max_step
        head_position = self.head_position if angle == 0 else self._rotate(self.center, self.head_position, angle)
        self.head.transform.update(head_position)
        points = self._calculate_points(self.center, self.tail.r, head_position, self.head.r)
        self.body.points = points

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
        self.head.render(screen, self.material)
        self.body.render(screen, self.material)
        self.tail.render(screen, self.material)
