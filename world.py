import random
from plant import Plant


class World:
    def __init__(self, seed: int, config):
        random.seed(seed)
        self.width = config.world_width
        self.height = config.world_height
        self.fields = [[list() for _ in range(self.width)] for _ in range(self.height)]
        self.growth_rate = config.plant_growth

        # generating random coords for plants
        coords = [(i, j) for i in range(self.height) for j in range(self.width)]
        k = (config.growth_percentage * self.width * self.height) // 100
        plant_coords = random.sample(coords, k)

        # adding plant instances to coresponding fields
        for coords in plant_coords:
            self.fields[coords[0]][coords[1]].append(Plant(list(coords)))

