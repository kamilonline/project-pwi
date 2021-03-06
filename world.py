import random
from config import WorldConfig
from organism import *


class World:
    def __init__(self, world_config: WorldConfig, plant_config: PlantConfig, organism_config: OrganismConfig):
        random.seed(world_config.seed)
        self.width = world_config.world_width
        self.height = world_config.world_height
        self.fields = [[list() for _ in range(self.width)] for _ in range(self.height)]

        # dictionaries initialization
        # {generation index : {id: entitiy instance}}
        self.plants = {0: {}}
        self.organisms = {0: {}}
        self.generation_colors = {0: (random.randint(128, 255),
                                      random.randint(128, 255),
                                      random.randint(128, 255))}

        # list of all possible coords
        coords = [(i, j) for i in range(self.height) for j in range(self.width)]

        Plant.initialize_class_atributes(plant_config)
        self.initialize_plants(coords, plant_config)

        Organism.initialize_class_atributes(organism_config)
        self.initialize_organisms(coords, organism_config)

    def initialize_plants(self, coords: list, plant_config: PlantConfig):
        generation = 0

        # generating random coords for plants
        k = int(plant_config.plant_percentage * self.width * self.height)
        plant_coords = random.sample(coords, k)

        # adding plant instances to corresponding fields
        for id, coords_iter in enumerate(plant_coords):
            plant = Plant(generation,
                          id,
                          list(coords_iter))
            self.fields[coords_iter[0]][coords_iter[1]].append(plant)
            self.plants[generation][id] = plant

    def initialize_organisms(self, coords: list, organism_config: OrganismConfig):
        generation = 0

        # generating random coords for organisms
        k = int(organism_config.organism_percentage * self.width * self.height)
        organisms_coords = random.sample(coords, k)

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

    def update_generation_colors(self):
        for generation in self.organisms.keys():
            if generation not in list(self.generation_colors.keys()):
                self.generation_colors[generation] = (random.randint(128, 255),
                                                      random.randint(128, 255),
                                                      random.randint(128, 255))

    def shuffle_organisms(self):
        result = []
        for generation in self.organisms.values():
            for organism in generation.values():
                result.append(organism)
        random.shuffle(result)
        return result

    def update(self, time_delta):
        randomized_organism_list = self.shuffle_organisms()
        if not randomized_organism_list:
            return 0
        Plant.frame_count += 1
        if Plant.frame_count >= Plant.growth:
            coords = [(i, j) for i in range(self.height) for j in range(self.width)]
            Plant.frame_count = 0
            new_plant = Plant.grow(self.plants, random.choice(coords))
            self.fields[new_plant.coords[0]][new_plant.coords[1]].append(new_plant)
        for organism in randomized_organism_list:

            if organism is not None:
                organism.update(time_delta, self.organisms, self.plants, self.fields)
        self.update_generation_colors()