import numpy as np
import pygame

from engine.Transform import Transform
from engine.Material import Material
from engine.shapes import Shape
from utils import is_2d_array


class Entity(pygame.sprite.Sprite):

    def __init__(self, shape: Shape, material: Material, mass: int, velocity: np.ndarray = None,
                 force: np.ndarray = None, name="None"):
        super().__init__()
        assert isinstance(shape, Shape)
        self.shape = shape
        self.transform: Transform = self.shape.transform
        assert isinstance(material, Material)
        self.material = material
        assert type(mass) is int
        self.mass = mass
        self.velocity = is_2d_array(velocity, True)
        self._prev_velocity = self.velocity
        self.force = is_2d_array(force, True)
        assert type(name) is str
        self.name = name

    def draw(self, screen):
        self.shape.render(screen, self.material)

    def update(self, delta_time: float):
        if self.velocity is None or self.force is None:
            return
        assert type(delta_time) is float
        acc = self.force / self.mass
        position = self.transform.position + self.velocity * delta_time + acc * delta_time ** 2 / 2
        self._prev_velocity = self.velocity
        self.velocity = self.velocity + acc * delta_time
        self.transform.update(position)
        self.shape.update()

    def get_contact_normal(self, entity):
        return self.shape.get_normal(entity.shape)

    def collide(self, entity):
        return self.shape.collide(entity.shape)

    def revert(self):
        self.velocity = self._prev_velocity

    def reset(self):
        pass
