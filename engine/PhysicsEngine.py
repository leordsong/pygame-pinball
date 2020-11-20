from engine.Entity import Entity


class Contact:

    def __init__(self, body_a: Entity, body_b: Entity):
        self.body_a = body_a
        self.body_b = body_b
        self.restitution = max(body_a.material.restitution, body_b.material.restitution)

    def resolve(self, delta_t):
        t = 0
        for i in range(1, 1001):
            t = delta_t * i / 1000
            self.body_a.update(t)
            if self.body_a.collide(self.body_b):
                break

        normal = self.body_a.get_contact_normal(self.body_b)
        if normal is None:
            print("Cannot get normal for ", self.body_b.name)
            return
        delta_v = (-1 - self.restitution) * self.body_a.velocity.dot(normal)
        gm = delta_v * normal
        self.body_a.velocity = self.body_a.velocity + gm
        self.body_a.update(delta_t - t)


def get_contacts(ball: Entity, static_bodies: [Entity]):
    result = []
    for static in static_bodies:
        if ball.collide(static):
            result.append(Contact(ball, static))
    return result
