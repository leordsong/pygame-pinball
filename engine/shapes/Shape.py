import numpy as np

from engine.Material import Material
from engine.Transform import Transform


class Shape:

    def __init__(self, transform: Transform, name: str):
        assert isinstance(transform, Transform)
        self.transform = transform
        assert type(name) is str
        self.name = name

    def update(self):
        pass

    def render(self, ctx, material: Material):
        raise Exception("draw is not implemented for ", self)

    def is_point_in_shape(self, point: np.ndarray) -> bool:
        raise Exception("is_point_in_shape is not implemented for ", self)

    def collide(self, shape):
        raise Exception("collide is not implemented for ", self, " and ", shape)

    def get_normal(self, shape):
        raise Exception("get_normal is not implemented for ", self, " and ", shape)

    def __str__(self):
        return self.name
