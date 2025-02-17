import pygame as pg

from control.states_control import States
from control.states.main_menu_states._main_menu_manager_ import Main_menu_manager
from control.views.main_menu_views.main_menu_display import Main_menu_display

from control.__control_settings__ import LANGUAGES_DICT, SCREEN_RESOLUTION_DICT

class Preferences_menu(States, Main_menu_manager, Main_menu_display):
    def __init__(self):
        """
            states all navigation paths and options to create buttons for,
            as well as their placement on the screen
        """
        States.__init__(self)
        Main_menu_manager.__init__(self)
    
    def cleanup(self):
        """
            cleans up all menu related data
        """
        pass

    def startup(self):
        """
            initiates all menu related data
        """
        self.init_config()
        self.init_main_menu_display()
        self.settings_in_preferences = self.settings.copy()
        self.init_preferences_menu_object()

    def get_event(self, event):
        """
            get all events and checks for custom conditions for the active
            menu only
        """
        if event.type == pg.QUIT:
            self.quit = True
        if event.type == pg.KEYDOWN:
            if pg.key.name(event.key) in self.return_keys and not self.quit:
                self.next = "title_screen"
                self.done = True
            if pg.key.name(event.key) in self.confirm_keys and\
                self.preferences_menu.selected_index == len(self.preferences_menu.next_list) - 1:
                self.select_option(self.preferences_menu)
            elif pg.key.name(event.key) in self.confirm_keys\
                and self.preferences_menu.selected_index == 4 and\
                    self.settings_in_preferences != self.settings:
                self.save_settings(self.settings_in_preferences)
                self.init_settings()
                self.init_config()
                self.startup()
            elif pg.key.name(event.key) in self.left_keys:
                self.change_settings(-1)
            elif pg.key.name(event.key) in self.right_keys:
                self.change_settings(1)

        self.preferences_menu.get_event_vertical(event)
    
    def change_settings(self, operant):
        OPTIONS = (("", self.settings_in_preferences['sfx_volume'], 'sfx_volume'),
                ("", self.settings_in_preferences['music_volume'], 'music_volume'),
                (LANGUAGES_DICT, self.settings_in_preferences['language'], 'language'),
                (SCREEN_RESOLUTION_DICT, self.settings_in_preferences['screen_resolution'], 'screen_resolution'))
        index = self.preferences_menu.selected_index

        if index in (0,1):
            current_setting_index = OPTIONS[index][1]
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
            self.settings_in_preferences['sfx_volume'] = selected_setting_index
        elif index == 1:
            self.settings_in_preferences['music_volume'] = selected_setting_index
        elif index == 2:
            self.settings_in_preferences['language'] = options_list[selected_setting_index]
        elif index == 3:
            self.settings_in_preferences['screen_resolution'] = options_list[selected_setting_index]
        
        self.update_preferences_menu_object()

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
        self.draw_preferences_screen()
        self.preferences_menu.draw_vertical_options()