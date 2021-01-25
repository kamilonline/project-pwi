class Entity:
    def __init__(self, generation: int, id: int, coords: list):
        self.generation = generation
        self.id = id
        self.coords = coords

    def destroy(self, entities, fields):
        entities[self.generation][self.id] = None

        i = self.coords[0]
        j = self.coords[1]
        index = fields[i][j].index(self)
        fields[i][j][index] = None
