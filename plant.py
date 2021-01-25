from config import PlantConfig
from entity import Entity


class Plant(Entity):
    growth = 0
    energy = 0

    def __init__(self, generation: int, id: int, coords: list):
        super().__init__(generation, id)
        self.position = coords

    @classmethod
    def initialize_class_atributes(cls, plant_config: PlantConfig):
        cls.growth = plant_config.plant_growth
        cls.energy = plant_config.plant_energy

