import random
from config import WorldConfig
from organism import *


class World:
    def __init__(self, seed: int, world_config: WorldConfig, plant_config: PlantConfig, organism_config: OrganismConfig):
        random.seed(seed)
        # todo: refactor this constructor to be shorter and more readable
        self.width = world_config.world_width
        self.height = world_config.world_height
        self.fields = [[list() for _ in range(self.width)] for _ in range(self.height)]

        # {generation index : {id: entitiy instance}}
        self.plants = {0: {}}
        self.organisms = {0: {}}
        self.growth_rate = plant_config.plant_growth

        # list of all possible coords
        coords = [(i, j) for i in range(self.height) for j in range(self.width)]
        k = int(plant_config.plant_percentage * self.width * self.height)
        plant_coords = random.sample(coords, k)

        generation = 0
        # adding plant instances to corresponding fields
        for id, coords_iter in enumerate(plant_coords):
            plant = Plant(generation,
                          id,
                          list(coords_iter))
            self.fields[coords_iter[0]][coords_iter[1]].append(plant)
            self.plants[generation][id] = plant

        # generating random coords for organisms
        k = int(organism_config.organism_percentage * self.width * self.height)
        organisms_coords = random.sample(coords, k)

        # set values from config to class attributes
        Organism.initialize_class_atributes(organism_config)

        # adding organism instances to corresponding fields

        for id, coords_iter in enumerate(organisms_coords):
            organism = Organism(generation,
                                id,
                                list(coords_iter),
                                organism_config.sight_distance,
                                organism_config.speed,
                                organism_config.energy_capacity
                                )

            self.fields[coords_iter[0]][coords_iter[1]].append(organism)
            self.organisms[generation][id] = organism
