from enum import Enum

from engine.Entity import Entity
from engine.shapes import Shape


class Contact:

    def __init__(self, body_a: Entity, body_b: Entity):
        self.body_a = body_a
        self.body_b = body_b
        self.restitution = max(body_a.material.restitution, body_b.material.restitution)

    def resolve(self, delta_t):
        normal = self.body_a.get_contact_normal(self.body_b)
        if normal is None:
            return
        delta_v = (-1 - self.restitution) * self.body_a.velocity.dot(normal)
        gm = delta_v * normal
        self.body_a.velocity = self.body_a.velocity + gm


class ContactType(Enum):
    CircleCircle = 0
    CircleRect = 1
    CirclePoly = 2
    Unknown = -1


def get_contacts(ball: Entity, static_bodies: [Entity]):
    result = []
    for static in static_bodies:
        if ball.collide(static):
            result.append(Contact(ball, static))
    return result


def is_colliding(shape_a: Shape, shape_b: Shape):
    return False


def get_normal(shape_a: Shape, shape_b: Shape):
    return False
