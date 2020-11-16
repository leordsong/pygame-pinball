from engine import Entity, Material, Transform
from engine.shapes import Rectangle


class Valve(Entity):

    def __init__(self, shape: Rectangle, new_shape: Rectangle, material: Material, name):
        super().__init__(Transform(shape.position, 100), shape, material, name)
        self.original_shape = shape
        self.new_shape = new_shape

    def trigger(self):
        self.shape = self.new_shape
        self.transform.position = self.shape.position

    def initialize(self):
        self.shape = self.original_shape
        self.transform.position = self.shape.position
