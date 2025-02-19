import pygame as pg

from game.views.display import Display
from game.models.menu_models.option_menu_model import Option_menu_model

from game._all_paths_ import LANGUAGES_DICT, SCREEN_RESOLUTION_DICT

class Main_menues_display(Display):
    """
        Class for managing the main menus display. It includes the title menu, preferences menu, and load menu.
    """
    def init_main_menu_display(self):
        Display.__init__(self)
        self.init_root_variables_main_menu()
        self.load_graphics_main_menues()
    
    def init_root_variables_main_menu(self):
        """
            Sets up initial variables for title menu, preferences menu, and load menu
        """

        self.title_menu_variables : tuple = (
            self.width*0.25, self.height*0.4, self.height*0.1
        )
        self.preferences_menu_variables : tuple = (
            self.width*0.5, self.height*0.15, self.height*0.12
        )
        self.load_menu_variables : tuple = (
            self.width*0.5, self.height/3, 75
        )

    def init_title_menu_object(self):
        self.title_menu = Option_menu_model(
            self.title_menu_variables,
            [self.dialogs['play'], self.dialogs['options'], self.dialogs['quit']],
            ["load_menu", "options", "quit"]
        )
        self.title_menu.update_colors((0,0,0), (255,255,0))
    
    def init_preferences_menu_object(self):
        options, next_list = self.init_render_option_preferences_menu()
        self.preferences_menu = Option_menu_model(
            self.preferences_menu_variables,
            options, next_list
        )
        self.preferences_menu.update_colors((255,255,255),(32,215,192))
    def update_preferences_menu_object(self):
        options, next_list = self.init_render_option_preferences_menu()
        self.preferences_menu.update_options(
            options, next_list
        )

    def init_load_menu_object(self):
        options, next_list = self.init_render_option_load_menu()
        self.load_menu = Option_menu_model(
            self.load_menu_variables,
            options, next_list
        )
        self.load_menu.update_colors((0,0,0),(80,96,176))
    def update_load_menu_object(self):
        options, next_list = self.init_render_option_load_menu()
        self.load_menu.update_options(
            options, next_list
        )

    def init_render_option_preferences_menu(self):
        """
            Generates the options for the preferences menu based on the current settings
        """
        options = [
            self.dialogs['sfx volume'] + str(self.settings_in_preferences['sfx_volume']),
            self.dialogs['music volume'] + str(self.settings_in_preferences['music_volume']),
            self.dialogs['language'] + LANGUAGES_DICT[self.settings_in_preferences['language']],
            self.dialogs['screen resolution'] + SCREEN_RESOLUTION_DICT[self.settings_in_preferences['screen_resolution']],
            self.dialogs['apply'], 
            self.dialogs['back']
        ]
        next_list = ["", "", "", "", "", "title_menu"]
        return options, next_list

    def init_render_option_load_menu(self):
        """
            Generates the options for the load menu based on available saved games
        """
        options = [self.dialogs['new game']]
        next_list = ["new_game"]
        for player_save in self.player_saves_state:
            if player_save == {}:
                options.append("")
                next_list.append("")
            else:
                options.append(player_save['player'])
                next_list.append("launch_menu")
        options.append(self.dialogs['back'])
        next_list.append("title_menu")
        return options, next_list

    def load_graphics_main_menues(self):
        """
            Loads and scales the graphics for the title, preferences, and load menus.
        """
        self.titleimg=pg.image.load(self.GRAPHICS_PATH+"/media/"+"title screen.png")
        self.titleimg=pg.transform.scale(self.titleimg,(self.screen_width,self.screen_height))

        self.preferencesimg = pg.image.load(self.GRAPHICS_PATH+"/media/"+"preferences screen.png")
        self.preferencesimg=pg.transform.scale(self.preferencesimg,(self.screen_width,self.screen_height))

        self.loadimg=pg.image.load(self.GRAPHICS_PATH+"/media/"+"load screen.png")
        self.loadimg=pg.transform.scale(self.loadimg,(self.screen_width,self.screen_height))

    def draw_load_screen(self):
        self.loadimg=pg.transform.scale(self.loadimg,(self.screen_width,self.screen_height))
        self.screen.blit(self.loadimg,(0,0))

    def draw_title_screen(self):
        self.titleimg=pg.transform.scale(self.titleimg,(self.screen_width,self.screen_height))
        self.screen.blit(self.titleimg,(0,0))
    
    def draw_preferences_screen(self):
        self.preferencesimg=pg.transform.scale(self.preferencesimg,(self.screen_width,self.screen_height))
        self.screen.blit(self.preferencesimg, (0,0))
