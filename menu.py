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

        self.settings = pygame_gui.elements.ui_panel.UIPanel(relative_rect=pygame.Rect((0,0), self.options.resolution),
        starting_layer_height=1,
        manager=self.manager,
        visible=False)

        self.ui_menu()
        self.ui_settings()

        self.clock = pygame.time.Clock()
        self.running = True


    def ui_menu(self):
        self.manager.set_window_resolution(self.options.resolution)
        self.manager.clear_and_reset()

        self.start_button = pygame_gui.elements.UIButton(pygame.Rect((int((self.options.resolution[0]-150) / 2), int((self.options.resolution[1]-120) / 2)),
        (150, 50)),
        'Start simulation',
        self.manager)

        self.settings_button = pygame_gui.elements.UIButton(pygame.Rect(((self.options.resolution[0]-165) / 2, (self.options.resolution[1]-120) / 2 + 70),
        (165, 50)),
        'Simulation settings',
        self.manager)


    def ui_settings(self):
        self.close_settings_button = pygame_gui.elements.UIButton(pygame.Rect(((self.options.resolution[0]-165) / 2, (self.options.resolution[1]-100)),
        (165, 50)),
        'Close',
        self.manager,
        container = self.settings)

        self.test_slider = pygame_gui.elements.UIHorizontalSlider(pygame.Rect((int(self.options.resolution[0] / 2),
                                                            int(self.options.resolution[1] * 0.70)),
                                                            (240, 25)),
                                                            50.0,
                                                            (0.0, 100.0),
                                                            self.manager,
                                                            container=self.settings)

        self.slider_label = pygame_gui.elements.UILabel(pygame.Rect((int(self.options.resolution[0] / 2) + 250,
                                                int(self.options.resolution[1] * 0.70)),
                                                (27, 25)),
                                                str(int(self.test_slider.get_current_value())),
                                                self.manager,
                                                container=self.settings)


    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT: self.running = False

            self.manager.process_events(event)

            if event.type == pygame.USEREVENT:
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == self.start_button:
                        print('Starting simulation')

                    if event.ui_element == self.settings_button:
                        self.manager.root_container.hide()
                        self.settings.show()

                    

                    if event.ui_element == self.close_settings_button:
                        self.manager.root_container.show()
                        self.settings.hide()


    def run(self):
        while self.running:
            time_delta = self.clock.tick()/1000.0

            self.events()
            self.manager.update(time_delta)

            if self.test_slider.has_moved_recently:
                self.slider_label.set_text(str(int(self.test_slider.get_current_value())))

            self.window_surface.blit(self.background, (0, 0))
            self.manager.draw_ui(self.window_surface)
            pygame.display.update()
        

if __name__ == '__main__':
    app = App()
    app.run()
