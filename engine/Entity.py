import numpy as np
import pygame

from engine.Transform import Transform
from engine.Material import Material
from engine.shapes import Shape


class Entity(pygame.sprite.Sprite):

    def __init__(self, transform: Transform, shape: Shape, material: Material, name="None"):
        super().__init__()
        self.transform = transform
        self.shape = shape
        self.shape.update_position(self.transform.position)
        self.material = material
        self.name = name

    def draw(self, ctx):
        self.shape.draw(ctx, self.material)

    def update(self, delta_time):
        self.transform.update(delta_time)
        self.shape.update_position(self.transform.position)

    def get_contact_normal(self, entity):
        return self.shape.get_normal(entity.shape)

    def collide(self, entity):
        return self.shape.collide(entity.shape)

    def revert(self):
        self.transform.revert()
        self.shape.update_position(self.transform.position)

    def init_position(self, position):
        self.transform.position = position
        self.transform._prev_position = position
        self.transform.velocity = None if self.transform.velocity is None else np.array([0, 0])
        self.transform._prev_velocity = self.transform.velocity
        self.transform.force = np.array([0, 0])


