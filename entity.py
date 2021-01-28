class Entity:
    def __init__(self, generation: int, id: int, coords: list):
        self.generation = generation
        self.id = id
        self.coords = coords

    def destroy(self, entities, fields):
        # assigning None because destroy is called during iteration
        entities[self.generation][self.id] = None

        i = self.coords[0]
        j = self.coords[1]
        if self in fields[i][j]:
            fields[i][j].remove(self)
