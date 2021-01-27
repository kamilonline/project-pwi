from scenes import *
from world import *
import pygame_gui
from vectormath import Vector2


class Simulation(Scene):
    def __init__(self):
        self.simulation_field_size = 20  # in pixels
        self.world = World(WorldConfig(), PlantConfig(), OrganismConfig())
        print(self.world.fields)
        self.manager = pygame_gui.UIManager(pygame.display.get_window_size())
        self.create_background()

    def create_background(self):
        self.background = pygame.Surface(pygame.display.get_window_size())
        self.background.fill(self.manager.get_theme().get_colour('dark_bg'))
        self.simulation_surface = pygame.Surface((self.world.width * self.simulation_field_size,
                                                  self.world.height * self.simulation_field_size))

    def process_frame(self, time_delta, events):
        self.process_events(events)
        self.manager.update(time_delta)
        self.update_simulation(time_delta)
        self.draw_simulation()
        self.manager.draw_ui(pygame.display.get_surface())

    def process_events(self, events):
        for event in events:
            self.manager.process_events(event)

    def draw_background(self):
        center_offset = (self.background.get_size()[0] // 2 - self.simulation_surface.get_size()[0] // 2,
                         self.background.get_size()[1] // 2 - self.simulation_surface.get_size()[1] // 2)

        window = pygame.display.get_surface()
        window.blit(self.background, (0, 0))
        window.blit(self.simulation_surface, center_offset)

    def draw_entities(self):
        for x in range(self.world.width):
            for y in range(self.world.height):
                field_entities = self.world.fields[y][x]
                field_organisms = [i for i in field_entities if isinstance(i, Organism)]
                entity = None
                if not field_organisms and field_entities:
                    entity = field_entities[0]
                elif field_organisms:
                    entity = field_organisms[0]

                if entity:
                    self.draw_entity(entity)

    def draw_entity(self, entity):
        if isinstance(entity, Organism):
            self.draw_organism(entity)
        elif isinstance(entity, Plant):
            self.draw_plant(entity)
        else:
            raise Exception("invalid entity instance, unable to draw")

    def draw_organism(self, entity):
        color = (entity.energy_capacity, 0, 0)
        organism_coords = Vector2(entity.coords[1], entity.coords[0])
        position = organism_coords * self.simulation_field_size + Vector2(self.simulation_field_size, self.simulation_field_size) / 2.0
        pygame.draw.circle(self.simulation_surface, color, tuple(position), self.simulation_field_size / 2.0)

    def draw_plant(self, entity):
        color = (124, 252, 0)
        rect = pygame.Rect(entity.coords[1] * self.simulation_field_size,
                           entity.coords[0] * self.simulation_field_size,
                           self.simulation_field_size,
                           self.simulation_field_size)

        pygame.draw.rect(self.simulation_surface, color, rect)

    def update_simulation(self, time_delta):
        pass

    def draw_simulation(self):
        self.draw_background()
        self.draw_entities()


