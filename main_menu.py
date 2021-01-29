from simulation import *
import json

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
        self.load_from_config()
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

        self.exit_button = pygame_gui.elements.UIButton(
            pygame.Rect((int((pygame.display.get_window_size()[0] - 150) / 2),
                         int((pygame.display.get_window_size()[1] - 120))),
                        (150, 50)),
            'Exit',
            self.manager)

    def create_settings_menu(self):
        # todo: move settings elements to fill the fullscreen mode
        self.close_settings_button = pygame_gui.elements.UIButton(
            pygame.Rect(((pygame.display.get_window_size()[0] * 0.05), (pygame.display.get_window_size()[1] - 100)),
                        (165, 50)),
            'Close',
            self.manager,
            container=self.settings)
        self.save_settings_button = pygame_gui.elements.UIButton(
            pygame.Rect(((pygame.display.get_window_size()[0] * 0.05 + 200), (pygame.display.get_window_size()[1] - 100)),
                        (165, 50)),
            'Save',
            self.manager,
            container=self.settings)

        world_width_cords = (pygame.display.get_window_size()[0] * 0.05, pygame.display.get_window_size()[1] * 0.05)

        self.world_width = pygame_gui.elements.UIHorizontalSlider(pygame.Rect(world_width_cords, (240, 25)),
                                                                 self.world_config_dict["world_width"],
                                                                  (0.0, 64.0),
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
                                                                   self.world_config_dict["world_height"],
                                                                   (0.0, 64.0),
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

        world_seed_cords = (world_width_cords[0], world_width_cords[1] + 100)

        self.seed = pygame_gui.elements.UITextEntryLine(pygame.Rect(world_seed_cords, (105, 100)), self.manager,
                                                         object_id='#int', container=self.settings)
        self.seed.set_allowed_characters(['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'])
        self.seed.set_text_length_limit(11)
        self.seed.set_text(str(self.world_config_dict["seed"]))
        self.seed_label = pygame_gui.elements.UILabel(pygame.Rect(world_seed_cords[0] + 105, world_seed_cords[1] + 7.5, 80, 15), "Seed",
                                                       self.manager, container=self.settings)
        self.randomize_seed_settings_button = pygame_gui.elements.UIButton(
            pygame.Rect(((world_seed_cords[0] + 190), (world_seed_cords[1])),
                        (120, 30)),
            'Randomize',
            self.manager,
            container=self.settings)

        plant_percentage_cords = (world_seed_cords[0], world_seed_cords[1] + 100)

        self.plant_percentage = pygame_gui.elements.UITextEntryLine(pygame.Rect(plant_percentage_cords,
                                                                                (60, 100)),
                                                                    self.manager,
                                                                    container=self.settings,
                                                                    object_id='#float')
        self.plant_percentage.set_allowed_characters(['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '.'])
        self.plant_percentage.set_text_length_limit(5)
        self.plant_percentage.set_text(str(self.plant_config_dict["plant_percentage"]))
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
        self.plant_growth.set_text(str(self.plant_config_dict["growth"]))
        self.plant_growth_label = pygame_gui.elements.UILabel(
            pygame.Rect(plant_growth_cords[0] + 70, plant_growth_cords[1] + 7.5,
                        170, 15),
            "Plant growth (frames)",
            self.manager,
            container=self.settings)

        plant_energy_cords = (plant_growth_cords[0], plant_growth_cords[1] + 60)

        self.plant_energy = pygame_gui.elements.UIHorizontalSlider(pygame.Rect(plant_energy_cords, (240, 25)),
                                                                   self.plant_config_dict["energy"],
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
        self.initial_percentage_of_organisms.set_text(str(self.organism_config_dict["organism_percentage"]))
        self.initial_percentage_of_organisms_label = pygame_gui.elements.UILabel(
            pygame.Rect(cords[0] + 70, cords[1] + 7.5, 270, 15), "Initial percentage of organisms", self.manager,
            container=self.settings)

        cords = (cords[0], cords[1] + 40)
        self.sight_distance = pygame_gui.elements.UITextEntryLine(pygame.Rect(cords, (60, 100)), self.manager,
                                                                  object_id='#int', container=self.settings, )
        self.sight_distance.set_allowed_characters(['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'])
        self.sight_distance.set_text_length_limit(5)
        self.sight_distance.set_text(str(self.organism_config_dict["sight_distance"]))
        self.sight_distance_label = pygame_gui.elements.UILabel(pygame.Rect(cords[0] + 60, cords[1] + 7.5, 150, 15),
                                                                "Sight distance", self.manager, container=self.settings)

        cords = (cords[0], cords[1] + 40)
        self.speed = pygame_gui.elements.UITextEntryLine(pygame.Rect(cords, (60, 100)), self.manager,
                                                         object_id='#int', container=self.settings)
        self.speed.set_allowed_characters(['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'])
        self.speed.set_text_length_limit(5)
        self.speed.set_text(str(self.organism_config_dict["speed"]))
        self.speed_label = pygame_gui.elements.UILabel(pygame.Rect(cords[0] + 60, cords[1] + 7.5, 80, 15), "Speed",
                                                       self.manager, container=self.settings)

        cords = (cords[0], cords[1] + 40)
        self.mut_probability = pygame_gui.elements.UITextEntryLine(pygame.Rect(cords, (60, 100)), self.manager,
                                                                   object_id='#float', container=self.settings)
        self.mut_probability.set_allowed_characters(['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '.'])
        self.mut_probability.set_text_length_limit(5)
        self.mut_probability.set_text(str(self.organism_config_dict["mutation_probability"]))
        self.mut_probability_label = pygame_gui.elements.UILabel(pygame.Rect(cords[0] + 80, cords[1] + 7.5, 160, 15),
                                                                 "Mutation probability", self.manager,
                                                                 container=self.settings)

        cords = (cords[0], cords[1] + 55)
        self.budding_energy_treshold = pygame_gui.elements.UIHorizontalSlider(pygame.Rect(cords, (240, 25)), self.organism_config_dict["energy_threshold"],
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
        self.budding_time_treshold.set_text(str(self.organism_config_dict["time_threshold"]))
        self.budding_time_treshold_label = pygame_gui.elements.UILabel(
            pygame.Rect(cords[0] + 70, cords[1] + 7.5, 190, 15), "Budding time treshold", self.manager,
            container=self.settings)

        cords = (cords[0], cords[1] + 40)
        self.budding_probability = pygame_gui.elements.UITextEntryLine(pygame.Rect(cords, (60, 100)), self.manager,
                                                                       object_id='#float', container=self.settings)
        self.budding_probability.set_allowed_characters(['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '.'])
        self.budding_probability.set_text_length_limit(5)
        self.budding_probability.set_text(str(self.organism_config_dict["budding_probability"]))
        self.budding_probability_label = pygame_gui.elements.UILabel(
            pygame.Rect(cords[0] + 80, cords[1] + 7.5, 160, 15), "Budding probability", self.manager,
            container=self.settings)

        cords = (cords[0], cords[1] + 70)
        self.initial_energy_capacity = pygame_gui.elements.UIHorizontalSlider(pygame.Rect(cords, (240, 25)),
                                                                              self.organism_config_dict["energy_capacity"],
                                                                              (0.0, 255.0), self.manager,
                                                                              container=self.settings)
        self.initial_energy_capacity_number = pygame_gui.elements.UILabel(
            pygame.Rect((cords[0] + 250, cords[1]), (27, 25)),
            str(int(self.initial_energy_capacity.get_current_value())), self.manager, container=self.settings)
        self.initial_energy_capacity_label = pygame_gui.elements.UILabel(pygame.Rect(cords[0], cords[1] - 15, 240, 15),
                                                                         "Initial energy capacity", self.manager,
                                                                         container=self.settings)

        cords = (cords[0], cords[1] + 50)
        self.budding_energy_loss = pygame_gui.elements.UIHorizontalSlider(pygame.Rect(cords, (240, 25)),
                                                                          self.organism_config_dict["budding_loss"],
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
        self.walking_energy_loss = pygame_gui.elements.UIHorizontalSlider(pygame.Rect(cords, (240, 25)),
                                                                          self.organism_config_dict["walking_loss"],
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
        self.stationary_energy_loss = pygame_gui.elements.UIHorizontalSlider(pygame.Rect(cords, (240, 25)),
                                                                             self.organism_config_dict["stationary_loss"],
                                                                             (0.0, 255.0), self.manager,
                                                                             container=self.settings)
        self.stationary_energy_loss_number = pygame_gui.elements.UILabel(
            pygame.Rect((cords[0] + 250, cords[1]), (27, 25)),
            str(int(self.stationary_energy_loss.get_current_value())), self.manager, container=self.settings)
        self.stationary_energy_loss_label = pygame_gui.elements.UILabel(pygame.Rect(cords[0], cords[1] - 15, 240, 15),
                                                                        "Stationary energy loss", self.manager,
                                                                        container=self.settings)

        cords = (cords[0], cords[1] + 40)
        self.eating_threshold= pygame_gui.elements.UITextEntryLine(pygame.Rect(cords, (60, 100)), self.manager,
                                                         object_id='#float', container=self.settings)
        self.eating_threshold.set_allowed_characters(['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'])
        self.eating_threshold.set_text_length_limit(5)
        self.eating_threshold.set_text(str(self.organism_config_dict["eating_threshold"]))
        self.eating_threshold_label = pygame_gui.elements.UILabel(pygame.Rect(cords[0] + 70, cords[1] + 7.5, 160, 15), "Eating threshold",
                                                       self.manager, container=self.settings)


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

                    if event.ui_element == self.settings_button:
                        self.manager.root_container.hide()
                        self.settings.show()
                        self.settings.visible = True

                    if event.ui_element == self.close_settings_button:
                        self.manager.root_container.show()
                        self.settings.hide()
                        self.settings.visible = False

                    if event.ui_element == self.exit_button:
                        new_event = pygame.event.Event(pygame.USEREVENT,
                                                       user_type=EXIT_APP_EVENT)
                        pygame.event.post(new_event)

                    if event.ui_element == self.save_settings_button:
                        self.dump_to_config()

                    if event.ui_element == self.randomize_seed_settings_button:
                        if isinstance(self.seed, pygame_gui.elements.ui_text_entry_line.UITextEntryLine):
                            self.seed.set_text(str(random.randint(1, 99999)))


                if event.user_type == pygame_gui.UI_TEXT_ENTRY_CHANGED:
                    if event.ui_object_id == 'panel.#float':
                        if event.ui_element.get_text() == '.' or event.ui_element.get_text() == '': continue
                        try:
                            temp = float(event.ui_element.get_text())
                            if temp > 1: event.ui_element.set_text('1')
                        except:
                            event.ui_element.set_text('0')
    def dump_to_config(self):

        with open("config/world-config.json", "w") as file:

            self.world_config_dict["world_width"] = self.convert_sprites_to_values(self.world_width)
            self.world_config_dict["world_height"] = self.convert_sprites_to_values(self.world_height)
            self.world_config_dict["seed"] = self.convert_sprites_to_values(self.seed)
            json.dump(self.world_config_dict, file, indent=4)

        with open("config/plant-config.json", "w") as file:


            self.plant_config_dict["plant_percentage"] = self.convert_sprites_to_values(self.plant_percentage)
            self.plant_config_dict["growth"] = self.convert_sprites_to_values(self.plant_growth)
            self.plant_config_dict["energy"] = self.convert_sprites_to_values(self.plant_energy)

            json.dump(self.plant_config_dict, file, indent=4)

        with open("config/organism-config.json", "w") as file:

            self.organism_config_dict["organism_percentage"] = self.convert_sprites_to_values(self.initial_percentage_of_organisms)
            self.organism_config_dict["sight_distance"] = self.convert_sprites_to_values(self.sight_distance)
            self.organism_config_dict["speed"] = self.convert_sprites_to_values(self.speed)
            self.organism_config_dict["mutation_probability"] = self.convert_sprites_to_values(self.mut_probability)
            self.organism_config_dict["energy_threshold"] = self.convert_sprites_to_values(self.budding_energy_treshold)
            self.organism_config_dict["time_threshold"] = self.convert_sprites_to_values(self.budding_time_treshold)
            self.organism_config_dict["budding_probability"] = self.convert_sprites_to_values(self.budding_probability)
            self.organism_config_dict["energy_capacity"] = self.convert_sprites_to_values(self.initial_energy_capacity)
            # config_dict["eating_threshold"] =
            self.organism_config_dict["budding_loss"] = self.convert_sprites_to_values(self.budding_energy_loss)
            self.organism_config_dict["walking_loss"] = self.convert_sprites_to_values(self.walking_energy_loss)
            self.organism_config_dict["stationary_loss"] = self.convert_sprites_to_values(self.stationary_energy_loss)
            self.organism_config_dict['energy_threshold'] = self.convert_sprites_to_values(self.budding_energy_treshold)

            json.dump(self.organism_config_dict, file, indent=4)

    def load_from_config(self):
        with open("config/world-config.json",) as file:
            config_dict = json.load(file)

            self.world_config_dict = config_dict

            self.world_width = config_dict["world_width"]
            self.world_height = config_dict["world_height"]
            self.seed = self.world_config_dict["seed"]

        with open("config/plant-config.json") as file:
            config_dict = json.load(file)

            self.plant_config_dict = config_dict

            self.plant_growth = config_dict["growth"]
            self.plant_percentage = config_dict["plant_percentage"]
            self.plant_energy = config_dict["energy"]

        with open("config/organism-config.json") as file:
            config_dict = json.load(file)

            self.organism_config_dict = config_dict

            self.initial_percentage_of_organisms = config_dict["organism_percentage"]
            self.sight_distance = config_dict["sight_distance"]
            self.speed = config_dict["speed"]
            self.mut_probability = config_dict["mutation_probability"]
            self.budding_energy_threshold = config_dict["energy_threshold"]
            self.budding_time_threshold = config_dict["time_threshold"]
            self.budding_probability = config_dict["budding_probability"]
            self.initial_energy_capacity = config_dict["energy_capacity"]
            # self.eating_threshold = config_dict["eating_threshold"]
            self.budding_energy_loss = config_dict["budding_loss"]
            self.walking_energy_loss = config_dict["walking_loss"]
            self.stationary_energy_loss = config_dict["stationary_loss"]


    def convert_sprites_to_values(self, object):
        if isinstance(object, pygame_gui.elements.ui_horizontal_slider.UIHorizontalSlider):
            return int(object.get_current_value())
        elif isinstance(object, pygame_gui.elements.ui_text_entry_line.UITextEntryLine):
            if "." in object.allowed_characters:

                return float(object.get_text())
            elif "." not in object.allowed_characters:

                return int(object.get_text())
