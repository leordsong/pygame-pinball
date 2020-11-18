import numpy as np

from engine import Entity, Transform, Material
from engine.shapes import Rectangle


class Wall(Entity):
    
    def __init__(self, position: np.ndarray, width: float, height: float, material: Material, name: str):
        super().__init__(Rectangle(width, height, Transform(position)), material, 100, name=name)
