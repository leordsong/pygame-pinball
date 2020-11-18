import math

import numpy as np
import pygame

from engine import Material, Transform
from engine.shapes.Rectangle import Rectangle
from engine.shapes.Shape import Shape
from engine.shapes.ConvexPolygon import ConvexPolygon
from utils import is_2d_array


class Circle(Shape):

    def __init__(self, r: float, transform: Transform):
        super().__init__(transform, "Circle")
        assert type(r) is float
        self.r = r

    def render(self, ctx, material: Material):
        if material.image is not None:
            ctx.blit(material.image, self.transform.position - self.r)
        else:
            pygame.draw.circle(ctx, material.color, [self.transform.position[0], self.transform.position[1]], self.r)

    def collide(self, shape: Shape):
        if isinstance(shape, Circle):
            dist = np.linalg.norm(shape.transform.position - self.transform.position)
            return dist <= (self.r + shape.r)
        if isinstance(shape, Rectangle):
            rect = Rectangle(shape.width + 2 * self.r, shape.height,
                             Transform(shape.transform.position - np.array([self.r, 0])))
            if rect.is_point_in_shape(self.transform.position):
                return True
            rect = Rectangle(shape.width, shape.height + 2 * self.r,
                             Transform(shape.transform.position - np.array([0, self.r])))
            if rect.is_point_in_shape(self.transform.position):
                return True
            for point in shape.points:
                if self.is_point_in_shape(point):
                    return True
            return False
        if isinstance(shape, ConvexPolygon):
            return shape.is_point_in_shape(self.transform.position) or self._edges_cross_circle(shape.points)
        raise Exception("Unknown shape: " + str(shape))

    def is_point_in_shape(self, point: np.ndarray) -> bool:
        is_2d_array(point)
        dist = np.linalg.norm(point - self.transform.position)
        return dist <= self.r

    def _edges_cross_circle(self, points: np.ndarray):
        edges = points.shape[0]
        points_prime = np.append(points, points[0].reshape((1, 2)), axis=0)
        for i in range(edges):
            if self._edge_cross_circle(points_prime[i], points_prime[i + 1]):
                return True
        return False

    def _edge_cross_circle(self, p1: np.ndarray, p2: np.ndarray):
        d: np.ndarray = p2 - p1
        f: np.ndarray = p1 - self.transform.position

        a = d.dot(d)
        b = 2 * f.dot(d)
        c = f.dot(f) - self.r ** 2
        discriminant = b ** 2 - 4 * a * c
        if discriminant < 0:
            return False
        discriminant = math.sqrt(discriminant)
        t1 = (-b - discriminant) / (2 * a)
        t2 = (-b + discriminant) / (2 * a)
        return 0 <= t1 <= 1 or 0 <= t2 <= 1

    def get_normal(self, shape: Shape):
        if isinstance(shape, Circle):
            vector = self.transform.position - shape.transform.position
            dist = np.linalg.norm(shape.transform.position - self.transform.position)
            return vector / dist
        if isinstance(shape, ConvexPolygon):
            edges = shape.points.shape[0]
            points_prime = np.append(shape.points, shape.points[0].reshape((1, 2)), axis=0)
            for i in range(edges):
                if self._edge_cross_circle(points_prime[i], points_prime[i + 1]):
                    edge = points_prime[i] - points_prime[i + 1]
                    normal = np.array([-edge[1], edge[0]]) / np.linalg.norm(edge)
                    pc = self.transform.position - points_prime[i]
                    if pc.dot(normal) < 0:
                        normal = -normal
                    return normal
            return None
        raise Exception("Unknown shape: " + str(shape))
