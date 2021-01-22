import random
from Config import *
from plant import Plant


class World:
    def __init__(self, seed: int, world_config: WorldConfig, plant_config: PlantConfig, organism_config: OrganismConfig):
        random.seed(seed)
        self.width = world_config.world_width
        self.height = world_config.world_height
        self.fields = [[list() for _ in range(self.width)] for _ in range(self.height)]
        self.growth_rate = plant_config.plant_growth

        # generating random coords for plants
        coords = [(i, j) for i in range(self.height) for j in range(self.width)]
        k = (plant_config.plant_percentage * self.width * self.height) // 100
        plant_coords = random.sample(coords, k)

        # adding plant instances to coresponding fields
        for coords in plant_coords:
            self.fields[coords[0]][coords[1]].append(Plant(list(coords)))

