from enum import Enum


class Direction(Enum):
    up = (-1,0)
    down = (1,0)
    right = (0,1)
    left = (0,-1)

    @staticmethod
    def generate_direction(organism_coords: list, target_coords: tuple):
        x_distance = abs(organism_coords[0] - target_coords[0])
        y_distance = abs(organism_coords[1] - target_coords[1])

