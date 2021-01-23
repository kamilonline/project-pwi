from config import OrganismConfig


class Organism:
    mutation_probability = 0
    budding_energy_threshold = 0
    budding_time_threshold = 0
    budding_probability = 0
    eating_threshold = 0
    budding_loss = 0
    walking_loss = 0
    stationary_loss = 0
    eating_loss = 0

    def __init__(self, sight_distance, speed, energy_capacity):
        self.sight_distance = sight_distance
        self.speed = speed
        self.energy_capacity = energy_capacity

    @classmethod
    def initialize_class_atributes(cls, organism_config: OrganismConfig):
        cls.mutation_probability = organism_config.mutation_probability
        cls.budding_energy_threshold = organism_config.budding_energy_threshold
        cls.budding_time_threshold = organism_config.budding_time_threshold
        cls.budding_probability = organism_config.budding_probability
        cls.eating_threshold = organism_config.eating_threshold
        cls.budding_loss = organism_config.budding_loss
        cls.walking_loss = organism_config.walking_loss
        cls.stationary_loss = organism_config.stationary_loss
        cls.eating_loss = organism_config.eating_loss
