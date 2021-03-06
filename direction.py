from enum import Enum
import random
from math_util import *


class Direction(Enum):
    here = (0, 0)
    up = (-1, 0)
    down = (1, 0)
    right = (0, 1)
    left = (0, -1)

    @staticmethod
    def generate_direction(organism_coords, target_coords):
        if target_coords is None:
            direction = random.choice([i.value for i in Direction])
            return Direction(direction)
        x_distance = abs(organism_coords[0] - target_coords[0])
        y_distance = abs(organism_coords[1] - target_coords[1])
        result = [sign(target_coords[0] - organism_coords[0]), sign(target_coords[1] - organism_coords[1])]
        result[ReLU(sign(x_distance - y_distance))] = 0
        return Direction(tuple(result))
