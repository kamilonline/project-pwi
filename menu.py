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


        world_width_cords = (self.options.resolution[0] * 0.05, self.options.resolution[1] * 0.05)

        self.world_width = pygame_gui.elements.UIHorizontalSlider(pygame.Rect(world_width_cords,(240, 25)),
        50.0,
        (0.0, 100.0),
        self.manager,
        container=self.settings)   

        self.world_width_number = pygame_gui.elements.UILabel(pygame.Rect((world_width_cords[0] + 250, world_width_cords[1]), (27, 25)),
        str(int(self.world_width.get_current_value())),
        self.manager,
        container=self.settings)

        self.world_width_label = pygame_gui.elements.UILabel(pygame.Rect(world_width_cords[0], world_width_cords[1] - 15,
        240, 15),
        "World width",
        self.manager,
        container=self.settings)


        world_height_cords = (world_width_cords[0], world_width_cords[1] + 50)

        self.world_height = pygame_gui.elements.UIHorizontalSlider(pygame.Rect(world_height_cords,(240, 25)),
        50.0,
        (0.0, 100.0),
        self.manager,
        container=self.settings)   

        self.world_height_number = pygame_gui.elements.UILabel(pygame.Rect((world_height_cords[0] + 250, world_height_cords[1]), (27, 25)),
        str(int(self.world_height.get_current_value())),
        self.manager,
        container=self.settings)

        self.world_height_label = pygame_gui.elements.UILabel(pygame.Rect(world_height_cords[0], world_height_cords[1] - 15,
        240, 15),
        "World height",
        self.manager,
        container=self.settings)


        world_border_cords = (world_width_cords[0], world_width_cords[1] + 100)

        self.world_border = pygame_gui.elements.UIButton(pygame.Rect(world_border_cords,
        (60, 30)),
        '',
        self.manager,
        container = self.settings)

        self.world_border_label = pygame_gui.elements.UILabel(pygame.Rect(world_border_cords[0] + 70, world_border_cords[1] + 7.5,
        110, 15),
        "World border",
        self.manager,
        container=self.settings)


        plant_percentage_cords = (world_border_cords[0], world_border_cords[1] + 100)

        self.plant_percentage = pygame_gui.elements.UITextEntryLine(pygame.Rect(plant_percentage_cords,
        (60,100)),
        self.manager,
        container = self.settings,
        object_id = '#float')
        self.plant_percentage.set_allowed_characters(['0','1','2','3','4','5','6','7','8','9','.'])
        self.plant_percentage.set_text_length_limit(5)

        self.plant_percentage_label = pygame_gui.elements.UILabel(pygame.Rect(plant_percentage_cords[0] + 70, plant_percentage_cords[1] + 7.5,
        130, 15),
        "Plant percentage",
        self.manager,
        container=self.settings)


        plant_growth_cords = (plant_percentage_cords[0], plant_percentage_cords[1] + 30)       

        self.plant_growth = pygame_gui.elements.UITextEntryLine(pygame.Rect(plant_growth_cords,
        (60,100)),
        self.manager,
        container = self.settings,
        object_id = '#int')
        self.plant_growth.set_allowed_characters(['0','1','2','3','4','5','6','7','8','9'])

        self.plant_growth_label = pygame_gui.elements.UILabel(pygame.Rect(plant_growth_cords[0] + 70, plant_growth_cords[1] + 7.5,
        170, 15),
        "Plant growth (frames)",
        self.manager,
        container=self.settings)


        plant_energy_cords = (plant_growth_cords[0], plant_growth_cords[1] + 60)   

        self.plant_energy = pygame_gui.elements.UIHorizontalSlider(pygame.Rect(plant_energy_cords,(240, 25)),
        50.0,
        (0.0, 255.0),
        self.manager,
        container=self.settings)   

        self.plant_energy_number = pygame_gui.elements.UILabel(pygame.Rect((plant_energy_cords[0] + 250, plant_energy_cords[1]), (27, 25)),
        str(int(self.world_height.get_current_value())),
        self.manager,
        container=self.settings)

        self.plant_energy_label = pygame_gui.elements.UILabel(pygame.Rect(plant_energy_cords[0], plant_energy_cords[1] - 15,
        240, 15),
        "Initial plant energy",
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
                        self.settings.visible = True                    

                    if event.ui_element == self.close_settings_button:
                        self.manager.root_container.show()
                        self.settings.hide()
                        self.settings.visible = False
                        
                    if event.ui_element == self.world_border:
                        if event.ui_element.is_selected: 
                            event.ui_element.unselect()
                            self.world_border.set_text("False")
                        else: 
                            event.ui_element.select()
                            self.world_border.set_text("True")
            

                if event.user_type == pygame_gui.UI_TEXT_ENTRY_CHANGED:
                    if event.ui_object_id == 'panel.#float':
                        if event.ui_element.get_text() == '.' or event.ui_element.get_text() == '': continue
                        try:
                            temp = float(event.ui_element.get_text())
                            if temp > 1: event.ui_element.set_text('1')
                        except: event.ui_element.set_text('0') 


    def sliders(self):
        if self.settings.visible:
            if self.world_width.has_moved_recently: self.world_width_number.set_text(str(int(self.world_width.get_current_value())))
            if self.world_height.has_moved_recently: self.world_height_number.set_text(str(int(self.world_height.get_current_value())))
            if self.plant_energy.has_moved_recently: self.plant_energy_number.set_text(str(int(self.plant_energy.get_current_value())))


    def run(self):
        while self.running:
            time_delta = self.clock.tick()/1000.0

            self.events()
            self.manager.update(time_delta)

            self.sliders()

            self.window_surface.blit(self.background, (0, 0))
            self.manager.draw_ui(self.window_surface)
            pygame.display.update()
        


if __name__ == '__main__':
    app = App()
    app.run()
