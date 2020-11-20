import numpy as np
import math

from engine.utils import is_2d_array


class Transform:

    def __init__(self, position: np.ndarray, rotation: float = 0.0):
        self.position = is_2d_array(position)
        self._prev_position = self.position
        assert type(rotation) is float
        assert -math.pi <= rotation <= math.pi
        self.rotation = rotation

    def update(self, position):
        is_2d_array(position)
        self._prev_position = self.position
        self.position = position

    def revert(self):
        self.position = self._prev_position

