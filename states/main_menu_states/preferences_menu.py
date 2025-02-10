import pygame as pg
from control.states_control import States
from assets.__control_settings__ import LANGUAGES_DICT, SCREEN_RESOLUTION_DICT
from states.main_menu_states.__main_menu_manager__ import Main_menu_manager
pg.font.init()

class Preferences_menu(States, Main_menu_manager):
    def __init__(self):
        """
            states all navigation paths and options to create buttons for,
            as well as their placement on the screen
        """
        States.__init__(self)
        Main_menu_manager.__init__(self)
        self.next = "" # only for indication, changes based on chosen option
        self.back = "main_menu" # used for back button, never changes
        self.next_list = ["", "", "", "", "", "main_menu",]

        self.from_top = self.screen_rect.height / 12.5
        self.spacer = 60
    
    def init_render_options(self):
        self.options = [
            "Sound effects : " + str(self.sfx_volume_in_preferences),
            "Music : " + str(self.music_volume_in_preferences),
            "Language : " + LANGUAGES_DICT[self.language_in_preferences],
            "Resolution : " + SCREEN_RESOLUTION_DICT[self.screen_resolution_in_preferences],
            "Apply", 
            "back"
        ]
    
    def cleanup(self):
        """
            cleans up all menu related data
        """
        pass

    def startup(self):
        """
            initiates all menu related data
        """
        if self.previous == "game":
            self.back = "game"
        else:
            self.back = "main_menu"
        self.settings_in_preferences = self.settings.copy()
        self.sfx_volume_in_preference = self.sfx_volume
        self.music_volume_in_preference = self.music_volume
        self.language_in_preference = self.language
        self.screen_resolution_in_preference = self.screen_resolution
        self.init_render_options()
        self.pre_render_options()

    def get_event(self, event):
        """
            get all events and checks for custom conditions for the active
            menu only
        """
        if event.type == pg.QUIT:
            self.quit = True
        if event.type == pg.KEYDOWN:
            if event.key in [pg.K_ESCAPE, pg.K_LSHIFT] and not self.quit:
                self.next = self.back
                self.done = True
            if event.key in [pg.K_RETURN, pg.K_SPACE, pg.K_KP_ENTER]\
                and self.selected_index == 4 and\
                    self.settings_in_preferences != self.settings:
                self.save_settings(self.settings_in_preferences)
                self.init_settings()
                self.init_config()
            elif event.key in [pg.K_UP, pg.K_z]:
                self.change_selected_option(-1)
            elif event.key in [pg.K_DOWN, pg.K_s]:
                self.change_selected_option(1)
            elif event.key in [pg.K_LEFT, pg.K_q]:
                self.change_settings(-1)
            elif event.key in [pg.K_RIGHT, pg.K_d]:
                self.change_settings(1)

        self.get_event_menu(event)
    
    def change_settings(self, operant):
        OPTIONS = (("", self.sfx_volume_in_preferences, 'sfx_volume'),
                    ("", self.music_volume_in_preferences, 'music_volume'),
                    (LANGUAGES_DICT, self.language_in_preferences, 'language'),
                    (SCREEN_RESOLUTION_DICT, self.screen_resolution_in_preferences, 'screen_resolution'))
        index = self.selected_index

        if index in (0,1):
            option = [self.sfx_volume_in_preferences, self.music_volume_in_preferences]
            current_setting_index = option[index]
            selected_setting_index = current_setting_index + operant

            if selected_setting_index < 0:
                selected_setting_index = 0
            elif selected_setting_index > 10:
                selected_setting_index = 10

            self.settings_in_preferences[OPTIONS[index][2]] = selected_setting_index
            
        elif index in (2,3):
            options_list = list(OPTIONS[index][0].keys())
            current_setting_index = options_list.index(OPTIONS[index][1])
            selected_setting_index = current_setting_index + operant
            if selected_setting_index < 0:
                selected_setting_index = len(options_list) - 1
            elif selected_setting_index > len(options_list) - 1:
                selected_setting_index = 0
            
            self.settings_in_preferences[OPTIONS[index][2]] = options_list[selected_setting_index]

        if index == 0:
            self.sfx_volume_in_preferences = selected_setting_index
        elif index == 1:
            self.music_volume_in_preferences = selected_setting_index
        elif index == 2:
            self.language_in_preferences = options_list[selected_setting_index]
        elif index == 3:
            self.screen_resolution_in_preferences = options_list[selected_setting_index]

        self.init_render_options()
        self.pre_render_options()

    def update(self):
        """
            update the menu with all new informations such as hovering or
            selecting an option as well as playing a sound when happening,
            then launch draw method
        """
        self.update_menu()
        self.draw()
    
    def draw(self):
        """
            launch all display related scripts proper to this menu back
            the main_menu states shared scripts
        """
        self.draw_menu_options()