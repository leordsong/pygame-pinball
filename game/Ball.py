import numpy as np

from engine import Entity, Transform, Material
from engine.shapes import Circle


class Ball(Entity):

    def __init__(self, position: np.ndarray, r: float, material: Material, name="TheBall"):
        super().__init__(Transform(position, 1, np.array([0, 0]), np.array([0, 0])), Circle(r), material, name)

    def launch(self):
        self.transform.velocity = self.transform.velocity + np.array([0, -400])
        self.transform.force = self.transform.force + np.array([0, 40])
