import pygame as pg

from control.states_control import States
from control.states.main_menu_states._main_menu_manager_ import Main_menu_manager
from control.views.main_menu_views.main_menu_display import Main_menu_display
from game.pokemons.pokedex import Pokedex

pg.font.init()

class Load_menu(States, Main_menu_manager, Main_menu_display):
    def __init__(self):
        """
            inits values specific to the menu such as navigation and
            placement of options
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
        States.player_pokedex = self.player_pokedex

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