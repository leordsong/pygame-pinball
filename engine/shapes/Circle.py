import math

import numpy as np
import pygame

from engine import Material
from engine.shapes.Shape import Shape
from engine.shapes.Rectangle import Rectangle
from engine.shapes.ConvexPolygon import ConvexPolygon


class Circle(Shape):

    def __init__(self, r: float, position: np.ndarray = None):
        super().__init__(position)
        self.r = r

    def draw(self, ctx, material: Material):
        if material.image is not None:
            ctx.blit(material.image, self.position - self.r)
        else:
            pygame.draw.circle(ctx, material.color, self.position, self.r)

    def collide(self, shape: Shape):
        if isinstance(shape, Circle):
            dist = np.linalg.norm(shape.position - self.position)
            return dist <= (self.r + shape.r)
        if isinstance(shape, Rectangle):
            points = shape.get_points()
            return self._point_in_convex_polygon(points) or self._edges_cross_circle(points)
        if isinstance(shape, ConvexPolygon):
            return self._point_in_convex_polygon(shape.points) or self._edges_cross_circle(shape.points)
        raise Exception("Unknown shape: " + str(type(shape)))

    def _point_in_convex_polygon(self, points: np.ndarray):
        edges = points.shape[0]
        a = points[0]
        for i in range(edges-2):
            b = points[i + 1]
            c = points[i + 2]
            if self._point_in_triangle(a, b, c):
                return True
        return False

    def _point_in_triangle(self, a, b, c):
        as_x = self.position[0] - a[0]
        as_y = self.position[1] - a[1]

        s_ab = (b[0] - a[0]) * as_y - (b[1] - a[1]) * as_x > 0

        if ((c[0] - a[0]) * as_y - (c[1] - a[1]) * as_x > 0) == s_ab:
            return False

        if ((c[0] - b[0]) * (self.position[1] - b[1]) - (c[1] - b[1]) * (self.position[0] - b[0]) > 0) != s_ab:
            return False

        return True

    def _edges_cross_circle(self, points: np.ndarray):
        edges = points.shape[0]
        points_prime = np.append(points, points[0].reshape((1, 2)), axis=0)
        for i in range(edges):
            if self._edge_cross_circle(points_prime[i], points_prime[i + 1]):
                return True
        return False

    def _edge_cross_circle(self, p1: np.ndarray, p2: np.ndarray):
        d: np.ndarray = p2 - p1
        f: np.ndarray = p1 - self.position

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

    def get_normal(self, shape):
        if isinstance(shape, Circle):
            vector = self.position - shape.position
            dist = np.linalg.norm(shape.position - self.position)
            return vector / dist
        points = None
        if isinstance(shape, Rectangle):
            points = shape.get_points()
        if isinstance(shape, ConvexPolygon):
            points = shape.points
        if points is not None:
            edges = points.shape[0]
            points_prime = np.append(points, points[0].reshape((1, 2)), axis=0)
            for i in range(edges):
                if self._edge_cross_circle(points_prime[i], points_prime[i + 1]):
                    edge = points_prime[i] - points_prime[i + 1]
                    return np.array([-edge[1], edge[0]]) / np.linalg.norm(edge)
            return None
        raise Exception("Unknown shape: " + str(type(shape)))





