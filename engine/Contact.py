from engine import Entity


class Contact:

    def __init__(self, body_a: Entity, body_b: Entity):
        self.body_a = body_a
        self.body_b = body_b
        self.restitution = max(body_a.material.restitution, body_b.material.restitution)

    def resolve(self, delta_t):
        normal = self.body_a.get_contact_normal(self.body_b)
        if normal is None:
            return
        delta_v = (-1 - self.restitution) * self.body_a.transform.velocity.dot(normal)
        gm = delta_v * normal
        self.body_a.transform.velocity = self.body_a.transform.velocity + gm


def get_contacts(ball: Entity, static_bodies: [Entity]):
    result = []
    for static in static_bodies:
        if ball.collide(static):
            result.append(Contact(ball, static))
    return result
