from objects.Ploygon import Polygon
import math


class Flipper(Polygon):

    def __init__(self, center, points, angle, color, spd, name="Flipper"):
        super().__init__(points, angle, color, spd, name)
        self.center = center
        self.origin_points = points

    def rotate(self, active):
        if active:
            points = []
            for point in self.origin_points:
                points.append(self._rotate(self.center, point, self.get_angle()))
            self.points = points
        else:
            self.points = self.origin_points

    @staticmethod
    def _rotate(origin, point, angle):
        """
        Rotate a point counterclockwise by a given angle around a given origin.

        The angle should be given in radians.
        """
        ox, oy = origin
        px, py = point

        qx = ox + math.cos(angle) * (px - ox) - math.sin(angle) * (py - oy)
        qy = oy + math.sin(angle) * (px - ox) + math.cos(angle) * (py - oy)
        return [qx, qy]
