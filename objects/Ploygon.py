from pygame import gfxdraw
from objects.Entity import Entity


class Polygon(Entity):

    def __init__(self, points, angle, color, spd, name="none"):
        super().__init__(0, 0, color, spd, name)
        self.points = points
        self.angle = angle

    def get_angle(self):
        return self.angle

    def draw(self, ctx):
        gfxdraw.filled_polygon(ctx, self.points, self.color)
        gfxdraw.aapolygon(ctx, self.points, self.color)
