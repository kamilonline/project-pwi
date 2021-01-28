from config import PlantConfig
from entity import Entity


class Plant(Entity):
    growth = 0
    energy = 0
    frame_count = 0

    def __init__(self, generation: int, id: int, coords: list):
        super().__init__(generation, id, coords)

    @classmethod
    def initialize_class_atributes(cls, plant_config: PlantConfig):
        cls.growth = plant_config.plant_growth
        cls.energy = plant_config.plant_energy

    @staticmethod
    def grow(plants, coords):
        new_generation = list(plants.keys())[-1] + 1
        if new_generation in plants and plants[new_generation]:
            new_id = list(plants[new_generation].keys())[-1] + 1
        else:
            new_id = 0
            if new_generation not in plants:
                plants[new_generation] = {}

        return Plant(new_generation, new_id, coords)
