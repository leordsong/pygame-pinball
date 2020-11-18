import numpy as np

from engine.Transform import Transform
from engine.shapes import Circle, Shape
from utils import is_color_tuple

print(np.concatenate((np.arange(9), np.array([-1]))))
print(np.arange(9)[-1])
print(np.linalg.norm(np.array([3, 4])))

a = np.array([0, 0], dtype=np.float)
print(a.shape == (2,))
print(np.array([0, 0]).shape == (2,))
points = np.array([[3, 4], [3, 4], [3, 4]], dtype=np.float)
c = Circle(1.0, Transform(a))
print(isinstance(c, Shape))