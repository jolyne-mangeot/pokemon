import pygame as pg

from game.control.models_controller import Models_controller
from game.views.main_menu_views.main_menues_display import Main_menues_display
from game.control.main_game_controllers.main_menues_controller import Main_menues_controller

from game.models.pokemons.pokedex import Pokedex

class Load_menu(Models_controller, Main_menues_controller, Main_menues_display):
    def __init__(self):
        """
            inits values specific to the menu such as navigation and
            placement of options
        """
        Models_controller.__init__(self)
        Main_menues_controller.__init__(self)

    def cleanup(self):
        """
            cleans up all menu related data
        """
        pass

    def startup(self):
        """
            initiates all menu-related data
        """
        self.init_config()
        self.init_main_menu_display()
        self.player_saves_state = self.load_player_data()
        self.init_load_menu_object()

    def init_player_save(self):
        current_player = self.player_saves_state[self.load_menu.selected_index - 1]
        Pokedex.init_pokedex_data()
        self.player_pokedex = Pokedex(current_player)
        Models_controller.player_pokedex = self.player_pokedex

    def get_event(self, event):
        """
            get all pygame-related events proper to the menu before
            checking main menu shared events
        """
        if event.type == pg.QUIT:
            self.quit = True
        if event.type == pg.KEYDOWN:
            if pg.key.name(event.key) in self.return_keys and not self.quit\
                or pg.key.name(event.key) in self.confirm_keys and\
                    self.load_menu.selected_index == len(self.load_menu.next_list) - 1:
                self.select_option(self.load_menu)

            elif pg.key.name(event.key) in self.confirm_keys:
                if self.load_menu.next_list[self.load_menu.selected_index] == "new_game":
                    self.select_option(self.load_menu)
                else:
                    self.init_player_save()
                    self.select_option(self.load_menu)

        self.load_menu.get_event_vertical(event)
    
    def update(self):
        """
            trigger all changes such as mouse hover or changing selected
            option, done after having checked in control class change on
            done and quit attribute from menu_manager inheritance
        """
        self.update_menu()
        self.draw()
    
    def draw(self):
        """
            init all display related script
        """
        self.draw_load_screen()
        self.load_menu.draw_vertical_options()