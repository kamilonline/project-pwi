import json


class WorldConfig:
    def __init__(self):

        with open("config/world-config.json", encoding="utf-8-sig") as file:
            config_dict = json.load(file)
            self.world_width = config_dict["world_width"]
            self.world_height = config_dict["world_height"]
            self.plant_growth = config_dict["growth"]
            self.growth_percentage = config_dict["growth-percentage"]
            self.border = config_dict["border"]
