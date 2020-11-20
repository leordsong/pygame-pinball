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
            point = self._find_closet_point_to_rect(shape)
            dist = np.linalg.norm(point - self.transform.position)
            return dist <= self.r
        if isinstance(shape, ConvexPolygon):
            return shape.is_point_in_shape(self.transform.position) or self._edges_cross_circle(shape.points)
        raise Exception("Unknown shape: " + str(shape))

    def _find_closet_point_to_rect(self, rect: Rectangle):
        x, y = self.transform.position
        x_t, y_t = rect.transform.position
        if x < x_t:
            x = x_t
        elif x > (x_t + rect.width):
            x = x_t + rect.width
        if y < y_t:
            y = y_t
        elif y > (y_t + rect.height):
            y = y_t + rect.height
        return np.array([x, y])

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
        # check if the vertexes are in the circle
        if self.is_point_in_shape(p1):
            return True
        if self.is_point_in_shape(p2):
            return True
        # check if center is projected on the edge
        p = self._project_to_edge(p1, p2)
        if p is None:
            return False
        # check the distance is smaller than r
        dist = np.linalg.norm(p - self.transform.position)
        return dist <= self.r

    def _project_to_edge(self, p1: np.ndarray, p2: np.ndarray):
        # draw a perpendicular line onto to the edge
        p12 = p2 - p1
        p1c = self.transform.position - p1
        length = np.linalg.norm(p12)
        dot_value = p1c.dot(p12) / length ** 2
        p = p1 + dot_value * p12
        # check the point is between vertexes
        if (p[0] < p1[0] and p[0] < p2[0]) or (p[0] > p1[0] and p[0] > p2[0]):
            return None
        if (p[1] < p1[1] and p[1] < p2[1]) or (p[1] > p1[1] and p[1] > p2[1]):
            return None
        return p

    def get_normal(self, shape: Shape):
        if isinstance(shape, Circle):
            vector = self.transform.position - shape.transform.position
            dist = np.linalg.norm(vector)
            return vector / dist
        if isinstance(shape, Rectangle):
            point = self._find_closet_point_to_rect(shape)
            vector = self.transform.position - point
            dist = np.linalg.norm(vector)
            return vector / dist
        if isinstance(shape, ConvexPolygon):
            edges = shape.points.shape[0]
            points_prime = np.append(shape.points, shape.points[0].reshape((1, 2)), axis=0)
            points = []
            distances = []
            for i in range(edges):
                points.append(points_prime[i])
                distances.append(np.linalg.norm(points_prime[i] - self.transform.position))
                point = self._project_to_edge(points_prime[i], points_prime[i + 1])
                if point is not None:
                    vector = self.transform.position - point
                    dist = np.linalg.norm(vector)
                    points.append(point)
                    distances.append(dist)
            index: int = np.argmin(distances)
            point = points[index]
            vector = self.transform.position - point
            dist = np.linalg.norm(vector)
            return vector/dist
        raise Exception("Unknown shape: " + str(shape))
