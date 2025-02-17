import pygame as pg

from views.display import Display
from views._option_menu_class_ import Option_menu_class

from control.__control_settings__ import LANGUAGES_DICT, SCREEN_RESOLUTION_DICT

class Main_menu_display(Display):
    def init_main_menu_display(self):
        Display.__init__(self)
        self.init_root_variables_main_menu()
        self.load_graphics_main_menues()
    
    def init_root_variables_main_menu(self):
        width : int = self.screen_rect.width
        height : int = self.screen_rect.height

        self.title_menu_variables : tuple = (
            width*0.25, 240, 75
        )
        self.preferences_menu_variables : tuple = (
            width/2, 80, 75
        )
        self.load_menu_variables : tuple = (
            width/2, height/4, 75
        )

    def init_title_menu_object(self):
        self.title_menu = Option_menu_class(
            self.title_menu_variables,
            [self.dialogs['play'], self.dialogs['options'], self.dialogs['quit']],
            ["load_menu", "options", "quit"]
        )
        self.title_menu.update_colors((255,255,255), (32,215,192))
    
    def init_preferences_menu_object(self):
        options, next_list = self.init_render_option_preferences_menu()
        self.preferences_menu = Option_menu_class(
            self.preferences_menu_variables,
            options, next_list
        )
    def update_preferences_menu_object(self):
        options, next_list = self.init_render_option_preferences_menu()
        self.preferences_menu.update_options(
            options, next_list
        )

    def init_load_menu_object(self):
        options, next_list = self.init_render_option_load_menu()
        self.load_menu = Option_menu_class(
            self.load_menu_variables,
            options, next_list
        )
    def update_load_menu_object(self):
        options, next_list = self.init_render_option_load_menu()
        self.load_menu.update_options(
            options, next_list
        )

    def init_render_option_preferences_menu(self):
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
