import json


class WorldConfig:
    def __init__(self):

        with open("config/world-config.json", encoding="utf-8-sig") as file:
            config_dict = json.load(file)
            self.world_width = config_dict["world_width"]
            self.world_height = config_dict["world_height"]
            self.border = config_dict["border"]


class PlantConfig:
    def __init__(self):
        with open("config/plant-config.json", encoding="utf-8-sig") as file:
            config_dict = json.load(file)
            self.plant_growth = config_dict["growth"]
            self.plant_percentage = config_dict["plant-percentage"]
            self.plant_energy = config_dict["energy"]


class OrganismConfig:
    def __init__(self):
        with open("config/organism-config.json", encoding="utf-8-sig") as file:
            confid_dict = json.load(file)
            self.organism_percentage = confid_dict["organism_percentage"]
            self.sight_distance = confid_dict["sight_distance"]
            self.speed = confid_dict["speed"]
            self.mutation_probability = confid_dict["mutation_probability"]
            self.energy_threshold = confid_dict["energy_threshold"]
            self.time_threshold = confid_dict["time_threshold"]
            self.probability = confid_dict["probability"]
            self.energy_capacity = confid_dict["energy_capacity"]
            self.eating_threshold = confid_dict["eating_threshold"]
            self.budding_loss = confid_dict["budding_loss"]
            self.walking_loss = confid_dict["walking_loss"]
            self.stationary_loss = confid_dict["stationary_loss"]
            self.eating_loss = confid_dict["eating_loss"]
