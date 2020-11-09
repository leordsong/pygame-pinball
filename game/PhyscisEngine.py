from engine.shapes.ConvexPolygon import ConvexPolygon

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
        delta_v = (-1 - self.restitution) * self.ball.transform.velocity.dot(self.normal)
        gm = delta_v * self.normal
        self.ball.transform.velocity = self.ball.transform.velocity + gm


def get_contacts(ball: Ball, static_bodies: [Entity]):
    result = []
    for static in static_bodies:
        if ball.shape.collide(static.shape):
            result.append(Contact(ball, static))
    return result
