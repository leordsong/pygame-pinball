import numpy as np

from engine import Entity, Transform, Material
from engine.shapes import Circle
from pinball.Flipper import Flipper
from engine.utils import is_2d_array


class Ball(Entity):

    def __init__(self, position: np.ndarray, r: float, material: Material, mass=1, name="TheBall"):
        super().__init__(Circle(r, Transform(position)), material, mass, np.array([0, 0]), np.array([0, 0]), name)
        self.original_position = position

    def launch(self):
        if np.array_equal(self.transform.position, self.original_position):
            self.velocity = self.velocity + np.array([0, -400])
            self.force = np.array([0, 80])

    def collide(self, entity) -> bool:
        if isinstance(entity, Flipper):
            return entity.collide_ball(self)
        return super(Ball, self).collide(entity)

    def reset(self):
        is_2d_array(self.original_position)
        self.transform.position = self.original_position
        self.transform._prev_position = self.original_position
        self.velocity = None if self.velocity is None else np.array([0, 0])
        self._prev_velocity = self.velocity
        self.force = None if self.force is None else np.array([0, 0])
        self.shape.update()
