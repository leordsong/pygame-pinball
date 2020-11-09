import numpy as np

from engine import Entity, Transform, Material
from engine.shapes import Circle


class Bumper(Entity):

    def __init__(self, position: np.ndarray, material: Material, r=10, points=1, name="Bumper"):
        super().__init__(Transform(position, 10), Circle(r), material, name)
        self.points = points
