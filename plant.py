from config import PlantConfig


class Plant:
    growth = 0
    energy = 0

    def __init__(self, coords: list):
        self.position = coords

    @classmethod
    def initialize_class_atributes(cls, plant_config: PlantConfig):
        cls.growth = plant_config.plant_growth
        cls.energy = plant_config.plant_energy

