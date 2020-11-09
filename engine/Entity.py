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


