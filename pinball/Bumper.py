import numpy as np

from engine import Entity, Transform, Material
from engine.shapes import Circle


class Bumper(Entity):

    def __init__(self, shape, material: Material, points=1, name="Bumper"):
        super().__init__(shape, material, 100, name=name)
        assert type(points) is int
        self.points = points



# position: np.ndarray
# Circle(r, Transform(position))