import random
from config import OrganismConfig
from plant import *
from direction import *


class Organism(Entity):
    traits_names = ("sight_distance", "speed", "energy_capacity")
    mutation_probability = 0
    budding_energy_threshold = 0
    budding_time_threshold = 0
    budding_probability = 0
    eating_threshold = 0
    budding_loss = 0
    walking_loss = 0
    stationary_loss = 0

    def __init__(self, *args):
        if len(args) == 1:
            collection = args[0]
            if isinstance(collection, dict):
                collection = list(collection.values())
        else:
            collection = args

        super().__init__(collection[0], collection[1], collection[2])

        self.sight_distance = collection[3]
        self.speed = collection[4]
        self.energy_capacity = collection[5]

        self.energy = self.energy_capacity
        self.orientation = Direction(random.choice([i.value for i in Direction]))
        self.budding_frame_count = 0
        self.speed_frame_count = 0
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

    def reproduce(self, organisms: dict, fields):
        """
        creates copy of organism and mutates it according to parameters
        :return: instance of Organism class
        """
        self.energy -= Organism.budding_loss
        if self.energy < 0:
            self.energy = 0
            return
        parent = self
        self.budding_frame_count = 0

        attributes = vars(parent).copy()
        new_coords = parent.coords.copy()
        attributes["coords"] = new_coords
        attributes = attributes.copy()
        attributes["generation"] += 1
        new_generation = attributes["generation"]

        # prepare a place in organisms nested dictionary in World class
        if new_generation in organisms and organisms[new_generation]:
            attributes["id"] = list(organisms[new_generation].keys())[-1] + 1
        else:
            attributes["id"] = 0
            if new_generation not in list(organisms.keys()):
                organisms[new_generation] = {}
        if random.random() < Organism.mutation_probability:
            # create new mutated atributes
            attributes = list(self.__mutate_attributes(attributes).values())
        new_organism = Organism(attributes)
        fields[new_organism.coords[0]][new_organism.coords[1]].append(new_organism)
        organisms[new_organism.generation][new_organism.id] = new_organism

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

    def __check_distance(self, x, y):
        distance = abs(self.coords[0] - x) + abs(self.coords[1] - y)
        return distance

    def search_fields(self, fields):
        minimum_distance = self.sight_distance
        min_coords = None
        world_height = len(fields)
        world_width = len(fields[0])

        for x in range(-self.sight_distance, self.sight_distance + 1):
            field_x = self.coords[0] + x
            if field_x > world_height - 1 or field_x < 0:
                continue

            for y in range(-self.sight_distance, self.sight_distance + 1):
                field_y = self.coords[1] + y
                if field_y > world_width - 1 or field_y < 0:
                    continue
                
                # checking if there is a plant on a current field
                seen_field = fields[field_x][field_y]
                if seen_field:
                    for element in seen_field:
                        if isinstance(element, Plant) or (isinstance(element, Organism) and element.energy_capacity <= Organism.eating_threshold*self.energy_capacity):

                            # looking for a nearest edible element
                            distance = self.__check_distance(field_x, field_y)
                            if distance < minimum_distance:
                                minimum_distance = distance
                                min_coords = (field_x, field_y)
        return Direction.generate_direction(self.coords, min_coords)

    def move(self, direction: Direction, world_height: int, world_width: int, fields):

        if self.energy - Organism.walking_loss < 0:
            return
        self.energy -= Organism.walking_loss

        if self in fields[self.coords[0]][self.coords[1]]:
            fields[self.coords[0]][self.coords[1]].remove(self)
        else:
            return
        self.coords[0] = max(0, min(world_height-1, self.coords[0] + direction.value[0]))

        self.coords[1] = max(0, min(world_width-1, self.coords[1] + direction.value[1]))

        fields[self.coords[0]][self.coords[1]].append(self)

    def eat(self, element):
        self.energy += element.energy

    def __str__(self):
        result = f'g: {self.generation} id: {self.id} coords: {self.coords} sight: {self.sight_distance} speed {self.speed} cap: {self.energy_capacity} E: {self.energy}'
        return result

    def update(self, time_delta, organisms, plants, fields):
        self.energy -= self.stationary_loss
        if self.energy <= 0:
            self.destroy(organisms, fields)
            return

        direction = self.search_fields(fields)
        # eating
        if direction.name == "here":
            if self.energy < self.energy_capacity:
                for entity in fields[self.coords[0]][self.coords[1]]:
                    # check if is able to eat
                    if isinstance(entity, Plant):
                        self.eat(entity)
                        entity.destroy(plants, fields)
                    elif isinstance(entity, Organism) and entity.energy_capacity <= self.energy_capacity * self.eating_threshold:
                        self.eat(entity)
                        entity.destroy(organisms, fields)
        # reproduction
        if self.energy > self.budding_energy_threshold:
            self.budding_frame_count += 1
            if self.budding_frame_count >= self.budding_time_threshold:

                if random.random() < self.budding_probability:
                    self.reproduce(organisms, fields)

        else:
            self.budding_frame_count = 0

        if self.energy == 0:
            self.destroy(organisms, fields)
            return

        if direction.name != "here":
            self.speed_frame_count += 1
            if self.speed_frame_count >= int(1/self.speed):
                self.move(direction, len(fields), len(fields[0]), fields)
                self.speed_frame_count = 0

        if self.energy == 0:
            self.destroy(organisms, fields)
            return

