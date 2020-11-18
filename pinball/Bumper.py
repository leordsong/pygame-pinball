import numpy as np

from engine import Entity, Transform, Material
from engine.shapes import Circle


class Bumper(Entity):

    def __init__(self, position: np.ndarray, material: Material, r=10.0, points=1, name="Bumper"):
        super().__init__(Circle(r, Transform(position)), material, 100, name=name)
        assert type(points) is int
        self.points = points
