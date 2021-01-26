import json


class WorldConfig:
    def __init__(self):

        with open("config/world-config.json", encoding="utf-8-sig") as file:
            config_dict = json.load(file)
            self.world_width = config_dict["world_width"]
            self.world_height = config_dict["world_height"]
            self.seed = config_dict["seed"]


class PlantConfig:
    def __init__(self):
        with open("config/plant-config.json", encoding="utf-8-sig") as file:
            config_dict = json.load(file)
            self.plant_growth = config_dict["growth"]
            self.plant_percentage = config_dict["plant_percentage"]
            self.plant_energy = config_dict["energy"]


class OrganismConfig:
    def __init__(self):
        with open("config/organism-config.json", encoding="utf-8-sig") as file:
            config_dict = json.load(file)
            self.organism_percentage = config_dict["organism_percentage"]
            self.sight_distance = config_dict["sight_distance"]
            self.speed = config_dict["speed"]
            self.mutation_probability = config_dict["mutation_probability"]
            self.budding_energy_threshold = config_dict["energy_threshold"]
            self.budding_time_threshold = config_dict["time_threshold"]
            self.budding_probability = config_dict["probability"]
            self.energy_capacity = config_dict["energy_capacity"]
            self.eating_threshold = config_dict["eating_threshold"]
            self.budding_loss = config_dict["budding_loss"]
            self.walking_loss = config_dict["walking_loss"]
            self.stationary_loss = config_dict["stationary_loss"]
            self.eating_loss = config_dict["eating_loss"]
