from typing import Tuple

from engine.utils import is_color_tuple


class Material:

    def __init__(self, color: Tuple[int, int, int, int], image=None, restitution: float = 0.9):
        self.color = is_color_tuple(color)
        self.image = image
        assert type(restitution) is float
        self.restitution = restitution
