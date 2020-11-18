from engine import Entity, Material, Transform
from engine.shapes import Rectangle


class Valve(Entity):

    def __init__(self, shape: Rectangle, new_shape: Rectangle, material: Material, name):
        super().__init__(shape, material, 100, name=name)
        self.original_shape = shape
        self.new_shape = new_shape

    def trigger(self):
        self.shape = self.new_shape
        self.transform = self.shape.transform

    def reset(self):
        self.shape = self.original_shape
        self.transform = self.shape.transform
