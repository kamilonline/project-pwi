class World:
    def __init__(self, seed: int, config):
        self.width = config.world_width
        self.height = config.world_height
        self.fields = [list() for _ in range(self.height)]
        