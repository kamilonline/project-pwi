import pygame
import pygame_gui

class Options:
    def __init__(self):
        self.resolution = (800, 600)
        self.fullscreen = False



class App:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Project PWI")
        
        self.options = Options()
        if self.options.fullscreen: self.window_surface = pygame.display.set_mode(self.options.resolution, pygame.FULLSCREEN)
        else: self.window_surface = pygame.display.set_mode(self.options.resolution)

        self.manager = pygame_gui.UIManager(self.options.resolution)
   
        self.background = pygame.Surface(self.options.resolution)
        self.background.fill(self.manager.get_theme().get_colour('dark_bg'))

        self.ui()

        self.clock = pygame.time.Clock()
        self.running = True


    def ui(self):
        self.manager.set_window_resolution(self.options.resolution)
        self.manager.clear_and_reset()

        self.start_button = pygame_gui.elements.UIButton(pygame.Rect((int((self.options.resolution[0]-150) / 2),
                                                        int((self.options.resolution[1]-120) / 2)),
                                                        (150, 50)),
                                                        'Start simulation',
                                                        self.manager)

        self.settings_button = pygame_gui.elements.UIButton(pygame.Rect(((self.options.resolution[0]-165) / 2,
                                                        (self.options.resolution[1]-120) / 2 + 70),
                                                        (165, 50)),
                                                        'Simulation settings',
                                                        self.manager)


    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT: self.running = False

            self.manager.process_events(event)

            if event.type == pygame.USEREVENT:
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == self.start_button:
                        print('Starting simulation')
                    if event.ui_element == self.settings_button:
                        print('Showing settings')


    def run(self):
        while self.running:
            time_delta = self.clock.tick()/1000.0

            self.events()
            self.manager.update(time_delta)

            self.window_surface.blit(self.background, (0, 0))
            self.manager.draw_ui(self.window_surface)
            pygame.display.update()
        

if __name__ == '__main__':
    app = App()
    app.run()
