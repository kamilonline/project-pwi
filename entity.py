class Entity:
    def __init__(self, generation: int, id: int):
        self.generation = generation
        self.id = id
    # todo: implement death without deleting ids from world dictionaries
