import numpy as np

from engine import Entity, Transform, Material
from engine.shapes import Circle
from game.Flipper import Flipper


class Ball(Entity):

    def __init__(self, position: np.ndarray, r: float, material: Material, name="TheBall"):
        super().__init__(Transform(position, 1, np.array([0, 0]), np.array([0, 0])), Circle(r), material, name)

    def launch(self):
        self.transform.velocity = self.transform.velocity + np.array([0, -400])
        self.transform.force = np.array([0, 40])

    def collide(self, entity):
        if isinstance(entity, Flipper):
            return self.shape.collide(entity.shape) or self.shape.collide(entity.body_shape) or self.shape.collide(
                entity.head_shape)
        return super(Ball, self).collide(entity)

    def get_contact_normal(self, entity):
        if isinstance(entity, Flipper):
            if self.shape.collide(entity.body_shape):
                return self.shape.get_normal(entity.body_shape)
            elif self.shape.collide(entity.head_shape):
                return self.shape.get_normal(entity.body_shape)
        return super(Ball, self).get_contact_normal(entity)
