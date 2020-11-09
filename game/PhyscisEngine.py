import numpy as np

from engine import Entity
from game.Ball import Ball


class Contact:

    def __init__(self, ball: Ball, static: Entity):
        self.ball = ball
        self.static = static
        self.normal = ball.shape.get_normal(static.shape)
        self.restitution = max(ball.material.restitution, static.material.restitution)

    def resolve(self):
        if self.normal is None:
            return
        print(self.normal)
        vc = (-1) * self.ball.transform.velocity * self.normal
        vc_prime = self.restitution * vc
        delta_v = vc - vc_prime
        inverse_mass = 1 / self.ball.transform.mass + 1 / self.static.transform.mass
        impulse = delta_v / inverse_mass
        gm = self.normal * impulse
        self.ball.transform.velocity = self.ball.transform.velocity + gm / self.ball.transform.mass


def get_contacts(ball: Ball, static_bodies: [Entity]):
    result = []
    for static in static_bodies:
        if ball.shape.collide(static.shape):
            result.append(Contact(ball, static))
    return result
