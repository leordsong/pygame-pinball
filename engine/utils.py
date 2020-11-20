from typing import Optional, Tuple

import numpy as np


def is_2d_array(array: Optional[np.ndarray], nullable: bool = False) -> Optional[np.ndarray]:
    """
    Check if it is a numpy 2d array

    :param array: the array to check
    :param nullable: whether the array is nullable
    :return: True if the array is a numpy 2d array, False otherwise
    """
    if array is None and nullable:
        return array
    assert type(array) is np.ndarray
    assert array.shape == (2,)
    return array


def is_polygon_array(points: np.ndarray) -> np.ndarray:
    """
    Check if it is a numpy array for polygon points

    :param points: the array to check
    :return: True if the array is a numpy array for polygon points, False otherwise
    """
    assert type(points) is np.ndarray
    assert len(points.shape) == 2
    assert points.shape[0] >= 3
    assert points.shape[1] == 2
    return points


def is_color_tuple(color: Tuple[int, int, int, int]) -> Tuple[int, int, int, int]:
    assert type(color) is tuple
    assert len(color) is 4
    assert type(color[0]) is int
    assert type(color[1]) is int
    assert type(color[2]) is int
    assert type(color[3]) is int
    return color
