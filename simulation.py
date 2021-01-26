from scenes import *
from world import *
import pygame_gui


class Simulation(Scene):
    def __init__(self):
        self.world = World(WorldConfig(), PlantConfig(), OrganismConfig())
        self.manager = pygame_gui.UIManager(pygame.display.get_window_size())
        self.background = pygame.Surface(pygame.display.get_window_size())
        self.background.fill(self.manager.get_theme().get_colour('dark_bg'))
        self.simulation_surface = pygame.Surface((self.world.width, self.world.height))

    def process_frame(self, time_delta, events):
        self.process_events(events)
        self.manager.update(time_delta)
        self.draw_background()
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

    def update_simulation(self, time_delta):
        pass

    def draw_simulation(self):
        self.draw_background()


