import numpy as np


class Transform:

    def __init__(self, position: np.ndarray, mass: int, velocity: np.ndarray = None, force: np.ndarray = None):
        self.position = position
        self._prev_position = position
        self.velocity = velocity
        self._prev_velocity = velocity
        self.mass = mass
        self.force = force

    def update(self, delta_time):
        if self.velocity is None or self.force is None:
            return
        self._prev_position = self.position
        self._prev_velocity = self.velocity
        acc = self.force / self.mass
        self.position = self.position + self.velocity * delta_time + acc * delta_time ** 2 / 2
        self.velocity = self.velocity + acc * delta_time

    def revert(self):
        self.position = self._prev_position
        self.velocity = self._prev_velocity
