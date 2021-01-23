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
        Organism.mutation_probability = organism_config.mutation_probability
        Organism.budding_energy_threshold = organism_config.budding_energy_threshold
        Organism.budding_time_threshold = organism_config.budding_time_threshold
        Organism.budding_probability = organism_config.budding_probability
        Organism.eating_threshold = organism_config.eating_threshold
        Organism.budding_loss = organism_config.budding_loss
        Organism.walking_loss = organism_config.walking_loss
        Organism.stationary_loss = organism_config.stationary_loss
        Organism.eating_loss = organism_config.eating_loss
