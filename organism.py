import random
from config import OrganismConfig


class Organism:
    traits_names = ("sight_distance", "speed", "energy_capacity")
    mutation_probability = 0
    budding_energy_threshold = 0
    budding_time_threshold = 0
    budding_probability = 0
    eating_threshold = 0
    budding_loss = 0
    walking_loss = 0
    stationary_loss = 0
    eating_loss = 0

    def __init__(self, *args):
        if len(args) == 1:
            collection = args[0]
            if isinstance(collection, dict):
                collection = list(collection.values())
        else:
            collection = args

        self.sight_distance = collection[0]
        self.speed = collection[1]
        self.energy_capacity = collection[2]

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

    def reproduce(self):
        """
        creates copy of organism and mutates it according to parameters
        :return: instance of Organism class
        """
        attributes = vars(self).copy()
        if random.random() < Organism.mutation_probability:
            # create new mutated atributes
            attributes = list(self.__mutate_attributes(attributes).values())

        new_organism = Organism(attributes)

        return new_organism

    @staticmethod
    def __mutate_attributes(attributes: dict):
        """
        :param attributes: dict of attribute names as keys and their values
        :return: dict with one of the attributes mutated
        """

        traits = [i for i in attributes.keys() if i in Organism.traits_names]

        # choose trait
        trait_to_mutate = random.choice(traits)
        change = random.random()
        sign = random.choice([-1, 1])
        mutated_trait = attributes[trait_to_mutate]

        # change the value of trait chosen to be mutated
        mutated_trait += sign * attributes[trait_to_mutate] * change

        # change data types if needed
        if trait_to_mutate == "sight_distance":
            mutated_trait = int(mutated_trait)

        elif trait_to_mutate == "energy_capacity":
            mutated_trait = min(255, int(mutated_trait))

        attributes[trait_to_mutate] = mutated_trait

        return attributes
