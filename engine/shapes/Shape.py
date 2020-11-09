import numpy as np

from engine.Material import Material


class Shape:

    def __init__(self, position: np.ndarray = None):
        self.position = position

    def update_position(self, position: np.array):
        self.position = position

    def draw(self, ctx, material: Material):
        pass

    def collide(self, shape):
        pass

    def get_normal(self, shape):
        pass
