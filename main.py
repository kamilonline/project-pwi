from main_menu import *
from simulation import *

class App:
    window = None
    clock = None
    active_scene = Scene()
    config = dict()

    def __init__(self):
        self.config = self.load_config()
        self.is_running = True
        self.init_pygame()
        self.change_scene(self.config["default scene"])
        self.main_loop()

    def init_pygame(self):
        pygame.init()
        pygame.display.set_caption("Project PWI")
        self.clock = pygame.time.Clock()
        self.window = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

    def load_config(self):
        return {
            "fps": 60,
            "default scene": MainMenu
        }

    def process_events(self):
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                self.is_running = False

            elif event.type == pygame.USEREVENT:
                if event.user_type == CHANGE_SCENE_EVENT:
                    self.change_scene(event.scene)
                elif event.user_type == EXIT_SIMULATION_EVENT:
                    self.change_scene(MainMenu)
                elif event.user_type == EXIT_APP_EVENT:
                    self.is_running = False
        return events

    def main_loop(self):

        while self.is_running:
            time_delta = self.clock.tick(self.config["fps"]) / 1000.0
            self.window.fill((0, 0, 0))
            self.active_scene.process_frame(time_delta, self.process_events())
            pygame.display.update()

    def change_scene(self, NewScene):  # new scene is a class inheriting from Scene
        self.active_scene.close_scene()
        self.active_scene = NewScene()


if __name__ == "__main__":
    app = App()