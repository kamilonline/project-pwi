from scenes import *
from world import *
import pygame_gui
from vectormath import Vector2


class Simulation(Scene):
    def __init__(self):
        self.simulation_field_size = 15  # in pixels
        self.world = World(WorldConfig(), PlantConfig(), OrganismConfig())
        #print(self.world.fields)
        self.manager = pygame_gui.UIManager(pygame.display.get_window_size())
        self.create_background()

    def create_background(self):
        self.background = pygame.Surface(pygame.display.get_window_size())
        self.background.fill(self.manager.get_theme().get_colour('dark_bg'))
        self.simulation_surface = pygame.Surface((self.world.width * self.simulation_field_size,
                                                  self.world.height * self.simulation_field_size))

        self.exit_button = pygame_gui.elements.UIButton(pygame.Rect((int((pygame.display.get_window_size()[0] - 150) / 2),
                                                                      int((pygame.display.get_window_size()[1] - 120))),
                                                                     (150, 50)),
                                                         'Exit',
                                                         self.manager)

    def process_frame(self, time_delta, events):
        self.process_events(events)
        self.manager.update(time_delta)
        self.update_simulation(time_delta)
        self.draw_simulation()
        self.manager.draw_ui(pygame.display.get_surface())


    def process_events(self, events):
        for event in events:
            self.manager.process_events(event)
            if event.type == pygame.USEREVENT:
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    new_event = pygame.event.Event(pygame.USEREVENT,
                                                   user_type=EXIT_SIMULATION_EVENT)
                    pygame.event.post(new_event)

    def draw_background(self):
        center_offset = (self.background.get_size()[0] // 2 - self.simulation_surface.get_size()[0] // 2,
                         self.background.get_size()[1] // 2 - self.simulation_surface.get_size()[1] // 2)

        window = pygame.display.get_surface()
        window.blit(self.background, (0, 0))
        generation_data_lines = self.get_generation_data()
        traits_data_lines = self.get_traits_data()
        window.blit(self.simulation_surface, center_offset)
        for index, line in enumerate(generation_data_lines):
            window.blit(line, (0, index*line.get_height()))
        for index, line in enumerate(traits_data_lines):
            window.blit(line, (self.background.get_width() - line.get_width(), index*line.get_height()*2))



    def draw_entities(self):
        self.simulation_surface.fill((0, 0, 0))
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
        color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
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
        self.world.update(time_delta)

    def draw_simulation(self):
        self.draw_background()

        self.draw_entities()

    def get_generation_data(self):
        text_color = (124, 185, 232)
        font = pygame.font.Font(None, 60)
        generations_count = [len([j for j in list(i.values()) if j is not None]) for i in list(self.world.organisms.values())]

        generations_data = [(index, str(i)) for index, i in enumerate(generations_count) if i > 0]
        lines = [font.render(str(line[0]) + ": " + line[1], True, text_color)for line in generations_data]
        return lines

    def get_traits_data(self):
        text_color = (124, 185, 232)
        font = pygame.font.Font(None, 60)
        organisms_list = [i for i in self.world.shuffle_organisms() if i is not None]


        average_sight_distance = sum([i.sight_distance for i in organisms_list]) / len(organisms_list)
        average_speed = sum([i.speed for i in organisms_list]) / len(organisms_list)
        average_energy_capacity = sum([i.energy_capacity for i in organisms_list]) /len(organisms_list)

        lines = ["average",
                 str(round(average_sight_distance, 2)) + " sight distance",
                 str(round(average_speed, 2)) + " speed",
                 str(round(average_energy_capacity, 2)) + " energy capacity"
                ]
        return [font.render(line, True, text_color) for line in lines]
