from simulation import *


class MainMenu(Scene):
    def __init__(self):
        self.manager = pygame_gui.UIManager(pygame.display.get_window_size())
        self.background = pygame.Surface(pygame.display.get_window_size())
        self.background.fill(self.manager.get_theme().get_colour('dark_bg'))

        self.settings = pygame_gui.elements.ui_panel.UIPanel(relative_rect=pygame.Rect((0, 0), pygame.display.get_window_size()),
                                                             starting_layer_height=1,
                                                             manager=self.manager,
                                                             visible=False)

        self.create_main_menu()
        self.create_settings_menu()

    def process_frame(self, time_delta, events):
        self.process_events(events)
        self.manager.update(time_delta)

        self.update_sliders_text()

        window = pygame.display.get_surface()
        window.blit(self.background, (0, 0))

        self.manager.draw_ui(window)

    def create_main_menu(self):
        self.manager.set_window_resolution(pygame.display.get_window_size())
        self.manager.clear_and_reset()

        self.start_button = pygame_gui.elements.UIButton(pygame.Rect((int((pygame.display.get_window_size()[0]-150) / 2), int((pygame.display.get_window_size()[1]-120) / 2)),
        (150, 50)),
        'Start simulation',
        self.manager)

        self.settings_button = pygame_gui.elements.UIButton(pygame.Rect(((pygame.display.get_window_size()[0]-165) / 2, (pygame.display.get_window_size()[1]-120) / 2 + 70),
        (165, 50)),
        'Simulation settings',
        self.manager)

    def create_settings_menu(self):
        # todo: move settings elements to fill the fullscreen mode
        self.close_settings_button = pygame_gui.elements.UIButton(
            pygame.Rect(((pygame.display.get_window_size()[0] * 0.05), (pygame.display.get_window_size()[1] - 100)),
                        (165, 50)),
            'Close',
            self.manager,
            container=self.settings)

        world_width_cords = (pygame.display.get_window_size()[0] * 0.05, pygame.display.get_window_size()[1] * 0.05)

        self.world_width = pygame_gui.elements.UIHorizontalSlider(pygame.Rect(world_width_cords, (240, 25)),
                                                                  50.0,
                                                                  (0.0, 100.0),
                                                                  self.manager,
                                                                  container=self.settings)

        self.world_width_number = pygame_gui.elements.UILabel(
            pygame.Rect((world_width_cords[0] + 250, world_width_cords[1]), (27, 25)),
            str(int(self.world_width.get_current_value())),
            self.manager,
            container=self.settings)

        self.world_width_label = pygame_gui.elements.UILabel(
            pygame.Rect(world_width_cords[0], world_width_cords[1] - 15,
                        240, 15),
            "World width",
            self.manager,
            container=self.settings)

        world_height_cords = (world_width_cords[0], world_width_cords[1] + 50)

        self.world_height = pygame_gui.elements.UIHorizontalSlider(pygame.Rect(world_height_cords, (240, 25)),
                                                                   50.0,
                                                                   (0.0, 100.0),
                                                                   self.manager,
                                                                   container=self.settings)

        self.world_height_number = pygame_gui.elements.UILabel(
            pygame.Rect((world_height_cords[0] + 250, world_height_cords[1]), (27, 25)),
            str(int(self.world_height.get_current_value())),
            self.manager,
            container=self.settings)

        self.world_height_label = pygame_gui.elements.UILabel(
            pygame.Rect(world_height_cords[0], world_height_cords[1] - 15,
                        240, 15),
            "World height",
            self.manager,
            container=self.settings)

        world_border_cords = (world_width_cords[0], world_width_cords[1] + 100)

        # todo: move elements to fill empty space left after deleting world border check box

        plant_percentage_cords = (world_border_cords[0], world_border_cords[1] + 100)

        self.plant_percentage = pygame_gui.elements.UITextEntryLine(pygame.Rect(plant_percentage_cords,
                                                                                (60, 100)),
                                                                    self.manager,
                                                                    container=self.settings,
                                                                    object_id='#float')
        self.plant_percentage.set_allowed_characters(['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '.'])
        self.plant_percentage.set_text_length_limit(5)

        self.plant_percentage_label = pygame_gui.elements.UILabel(
            pygame.Rect(plant_percentage_cords[0] + 70, plant_percentage_cords[1] + 7.5,
                        130, 15),
            "Plant percentage",
            self.manager,
            container=self.settings)

        plant_growth_cords = (plant_percentage_cords[0], plant_percentage_cords[1] + 30)

        self.plant_growth = pygame_gui.elements.UITextEntryLine(pygame.Rect(plant_growth_cords,
                                                                            (60, 100)),
                                                                self.manager,
                                                                container=self.settings,
                                                                object_id='#int')
        self.plant_growth.set_allowed_characters(['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'])

        self.plant_growth_label = pygame_gui.elements.UILabel(
            pygame.Rect(plant_growth_cords[0] + 70, plant_growth_cords[1] + 7.5,
                        170, 15),
            "Plant growth (frames)",
            self.manager,
            container=self.settings)

        plant_energy_cords = (plant_growth_cords[0], plant_growth_cords[1] + 60)

        self.plant_energy = pygame_gui.elements.UIHorizontalSlider(pygame.Rect(plant_energy_cords, (240, 25)),
                                                                   50.0,
                                                                   (0.0, 255.0),
                                                                   self.manager,
                                                                   container=self.settings)

        self.plant_energy_number = pygame_gui.elements.UILabel(
            pygame.Rect((plant_energy_cords[0] + 250, plant_energy_cords[1]), (27, 25)),
            str(int(self.world_height.get_current_value())),
            self.manager,
            container=self.settings)

        self.plant_energy_label = pygame_gui.elements.UILabel(
            pygame.Rect(plant_energy_cords[0], plant_energy_cords[1] - 15,
                        240, 15),
            "Initial plant energy",
            self.manager,
            container=self.settings)

        cords = (world_width_cords[0] + 400, world_width_cords[1])

        self.initial_percentage_of_organisms = pygame_gui.elements.UITextEntryLine(pygame.Rect(cords,
                                                                                               (60, 100)), self.manager,
                                                                                   object_id='#float',
                                                                                   container=self.settings)
        self.initial_percentage_of_organisms.set_allowed_characters(
            ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '.'])
        self.initial_percentage_of_organisms.set_text_length_limit(5)
        self.initial_percentage_of_organisms_label = pygame_gui.elements.UILabel(
            pygame.Rect(cords[0] + 70, cords[1] + 7.5, 270, 15), "Initial percentage of organisms", self.manager,
            container=self.settings)

        cords = (cords[0], cords[1] + 40)
        self.sight_distance = pygame_gui.elements.UITextEntryLine(pygame.Rect(cords, (60, 100)), self.manager,
                                                                  object_id='#float', container=self.settings, )
        self.sight_distance.set_allowed_characters(['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '.'])
        self.sight_distance.set_text_length_limit(5)
        self.sight_distance_label = pygame_gui.elements.UILabel(pygame.Rect(cords[0] + 60, cords[1] + 7.5, 150, 15),
                                                                "Sight distance", self.manager, container=self.settings)

        cords = (cords[0], cords[1] + 40)
        self.speed = pygame_gui.elements.UITextEntryLine(pygame.Rect(cords, (60, 100)), self.manager,
                                                         object_id='#float', container=self.settings)
        self.speed.set_allowed_characters(['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '.'])
        self.speed.set_text_length_limit(5)
        self.speed_label = pygame_gui.elements.UILabel(pygame.Rect(cords[0] + 60, cords[1] + 7.5, 80, 15), "Speed",
                                                       self.manager, container=self.settings)

        cords = (cords[0], cords[1] + 40)
        self.mut_probability = pygame_gui.elements.UITextEntryLine(pygame.Rect(cords, (60, 100)), self.manager,
                                                                   object_id='#float', container=self.settings)
        self.mut_probability.set_allowed_characters(['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '.'])
        self.mut_probability.set_text_length_limit(5)
        self.mut_probability_label = pygame_gui.elements.UILabel(pygame.Rect(cords[0] + 80, cords[1] + 7.5, 160, 15),
                                                                 "Mutation probability", self.manager,
                                                                 container=self.settings)

        cords = (cords[0], cords[1] + 55)
        self.budding_energy_treshold = pygame_gui.elements.UIHorizontalSlider(pygame.Rect(cords, (240, 25)), 50.0,
                                                                              (0.0, 255.0), self.manager,
                                                                              container=self.settings)
        self.budding_energy_treshold_number = pygame_gui.elements.UILabel(
            pygame.Rect((cords[0] + 250, cords[1]), (27, 25)),
            str(int(self.budding_energy_treshold.get_current_value())), self.manager, container=self.settings)
        self.budding_energy_treshold_label = pygame_gui.elements.UILabel(pygame.Rect(cords[0], cords[1] - 15, 240, 15),
                                                                         "Budding energy treshold", self.manager,
                                                                         container=self.settings)

        cords = (cords[0], cords[1] + 40)
        self.budding_time_treshold = pygame_gui.elements.UITextEntryLine(pygame.Rect(cords, (60, 100)), self.manager,
                                                                         container=self.settings)
        self.budding_time_treshold.set_allowed_characters(['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'])
        self.budding_time_treshold.set_text_length_limit(5)
        self.budding_time_treshold_label = pygame_gui.elements.UILabel(
            pygame.Rect(cords[0] + 70, cords[1] + 7.5, 190, 15), "Budding time treshold", self.manager,
            container=self.settings)

        cords = (cords[0], cords[1] + 40)
        self.budding_probability = pygame_gui.elements.UITextEntryLine(pygame.Rect(cords, (60, 100)), self.manager,
                                                                       object_id='#float', container=self.settings)
        self.budding_probability.set_allowed_characters(['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '.'])
        self.budding_probability.set_text_length_limit(5)
        self.budding_probability_label = pygame_gui.elements.UILabel(
            pygame.Rect(cords[0] + 80, cords[1] + 7.5, 160, 15), "Budding probability", self.manager,
            container=self.settings)

        cords = (cords[0], cords[1] + 70)
        self.initial_energy_capacity = pygame_gui.elements.UIHorizontalSlider(pygame.Rect(cords, (240, 25)), 50.0,
                                                                              (0.0, 255.0), self.manager,
                                                                              container=self.settings)
        self.initial_energy_capacity_number = pygame_gui.elements.UILabel(
            pygame.Rect((cords[0] + 250, cords[1]), (27, 25)),
            str(int(self.initial_energy_capacity.get_current_value())), self.manager, container=self.settings)
        self.initial_energy_capacity_label = pygame_gui.elements.UILabel(pygame.Rect(cords[0], cords[1] - 15, 240, 15),
                                                                         "Initial energy capacity", self.manager,
                                                                         container=self.settings)

        cords = (cords[0], cords[1] + 50)
        self.budding_energy_loss = pygame_gui.elements.UIHorizontalSlider(pygame.Rect(cords, (240, 25)), 50.0,
                                                                          (0.0, 255.0), self.manager,
                                                                          container=self.settings)
        self.budding_energy_loss_number = pygame_gui.elements.UILabel(pygame.Rect((cords[0] + 250, cords[1]), (27, 25)),
                                                                      str(int(
                                                                          self.budding_energy_loss.get_current_value())),
                                                                      self.manager, container=self.settings)
        self.budding_energy_loss_label = pygame_gui.elements.UILabel(pygame.Rect(cords[0], cords[1] - 15, 240, 15),
                                                                     "Budding energy loss", self.manager,
                                                                     container=self.settings)

        cords = (cords[0], cords[1] + 50)
        self.walking_energy_loss = pygame_gui.elements.UIHorizontalSlider(pygame.Rect(cords, (240, 25)), 50.0,
                                                                          (0.0, 255.0), self.manager,
                                                                          container=self.settings)
        self.walking_energy_loss_number = pygame_gui.elements.UILabel(pygame.Rect((cords[0] + 250, cords[1]), (27, 25)),
                                                                      str(int(
                                                                          self.walking_energy_loss.get_current_value())),
                                                                      self.manager, container=self.settings)
        self.walking_energy_loss_label = pygame_gui.elements.UILabel(pygame.Rect(cords[0], cords[1] - 15, 240, 15),
                                                                     "Walking energy loss", self.manager,
                                                                     container=self.settings)

        cords = (cords[0], cords[1] + 50)
        self.stationary_energy_loss = pygame_gui.elements.UIHorizontalSlider(pygame.Rect(cords, (240, 25)), 50.0,
                                                                             (0.0, 255.0), self.manager,
                                                                             container=self.settings)
        self.stationary_energy_loss_number = pygame_gui.elements.UILabel(
            pygame.Rect((cords[0] + 250, cords[1]), (27, 25)),
            str(int(self.stationary_energy_loss.get_current_value())), self.manager, container=self.settings)
        self.stationary_energy_loss_label = pygame_gui.elements.UILabel(pygame.Rect(cords[0], cords[1] - 15, 240, 15),
                                                                        "Stationary energy loss", self.manager,
                                                                        container=self.settings)

        cords = (cords[0], cords[1] + 50)
        self.eating_energy_loss = pygame_gui.elements.UIHorizontalSlider(pygame.Rect(cords, (240, 25)), 50.0,
                                                                         (0.0, 255.0), self.manager,
                                                                         container=self.settings)
        self.eating_energy_loss_number = pygame_gui.elements.UILabel(pygame.Rect((cords[0] + 250, cords[1]), (27, 25)),
                                                                     str(int(
                                                                         self.eating_energy_loss.get_current_value())),
                                                                     self.manager, container=self.settings)
        self.eating_energy_loss_label = pygame_gui.elements.UILabel(pygame.Rect(cords[0], cords[1] - 15, 240, 15),
                                                                    "Eating energy loss", self.manager,
                                                                    container=self.settings)


    def update_sliders_text(self):
        if self.settings.visible:
            if self.world_width.has_moved_recently: self.world_width_number.set_text(
                str(int(self.world_width.get_current_value())))
            if self.world_height.has_moved_recently: self.world_height_number.set_text(
                str(int(self.world_height.get_current_value())))
            if self.plant_energy.has_moved_recently: self.plant_energy_number.set_text(
                str(int(self.plant_energy.get_current_value())))

            if self.budding_energy_treshold.has_moved_recently: self.budding_energy_treshold_number.set_text(
                str(int(self.budding_energy_treshold.get_current_value())))
            if self.initial_energy_capacity.has_moved_recently: self.initial_energy_capacity_number.set_text(
                str(int(self.initial_energy_capacity.get_current_value())))
            if self.budding_energy_loss.has_moved_recently: self.budding_energy_loss_number.set_text(
                str(int(self.budding_energy_loss.get_current_value())))
            if self.walking_energy_loss.has_moved_recently: self.walking_energy_loss_number.set_text(
                str(int(self.walking_energy_loss.get_current_value())))
            if self.stationary_energy_loss.has_moved_recently: self.stationary_energy_loss_number.set_text(
                str(int(self.stationary_energy_loss.get_current_value())))
            if self.eating_energy_loss.has_moved_recently: self.eating_energy_loss_number.set_text(
                str(int(self.eating_energy_loss.get_current_value())))
    def process_events(self, events):
        for event in events:

            self.manager.process_events(event)

            if event.type == pygame.USEREVENT:
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == self.start_button:
                        new_event = pygame.event.Event(pygame.USEREVENT,
                                                       user_type=CHANGE_SCENE_EVENT,
                                                       scene=Simulation)
                        pygame.event.post(new_event)
                        print('Starting simulation')

                    if event.ui_element == self.settings_button:
                        self.manager.root_container.hide()
                        self.settings.show()
                        self.settings.visible = True

                    if event.ui_element == self.close_settings_button:
                        self.manager.root_container.show()
                        self.settings.hide()
                        self.settings.visible = False


                if event.user_type == pygame_gui.UI_TEXT_ENTRY_CHANGED:
                    if event.ui_object_id == 'panel.#float':
                        if event.ui_element.get_text() == '.' or event.ui_element.get_text() == '': continue
                        try:
                            temp = float(event.ui_element.get_text())
                            if temp > 1: event.ui_element.set_text('1')
                        except:
                            event.ui_element.set_text('0')