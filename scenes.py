from enum import Enum
import pygame
CHANGE_SCENE_EVENT = pygame.event.custom_type()


class Scene:
    def __init__(self):
        pass

    def close_scene(self):
        pass

    def process_frame(self, time_delta, events):
        pass



class Scenes(Enum):
    main_menu = 0
    simulation = 1