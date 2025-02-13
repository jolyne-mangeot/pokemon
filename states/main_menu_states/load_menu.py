import pygame as pg
from control.states_control import States
from states.main_menu_states.__main_menu_manager__ import Main_menu_manager
from game.pokemons.pokedex import Pokedex

pg.font.init()

class Load_menu(States, Main_menu_manager):
    def __init__(self):
        """
            inits values specific to the menu such as navigation and
            placement of options
        """
        States.__init__(self)
        Main_menu_manager.__init__(self)
        self.next = ""
        self.back = "main_menu"
        self.from_top = self.screen_rect.height / 4
        self.spacer = 75
    
    def init_render_option(self):
        self.options = [self.dialogs['new game']]
        self.next_list = ["new_game"]
        for player_save in self.player_saves_state:
            if player_save == {}:
                self.options.append("")
                self.next_list.append("")
            else:
                self.options.append(player_save['player'])
                self.next_list.append("launch_menu")
        self.options.append(self.dialogs['back'])
        self.next_list.append("main_menu")
    
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
        self.player_saves_state = self.load_player_data()
        self.init_render_option()
        self.pre_render_options()
        pass

    def get_event(self, event):
        """
            get all pygame-related events proper to the menu before
            checking main menu shared events
        """
        if event.type == pg.QUIT:
            self.quit = True
        if event.type == pg.KEYDOWN:
            if pg.key.name(event.key) in self.return_keys and not self.quit:
                self.next = self.back
                self.done = True
            if pg.key.name(event.key) in self.confirm_keys and self.selected_index in (0,1,2):
                if self.next_list[self.selected_index] == "new_game":
                    self.select_option()
                else:
                    current_player = self.player_saves_state[self.selected_index-1]
                    current_pokedex = Pokedex(current_player)
                    States.player_pokedex = current_pokedex
                    self.select_option()

        self.get_event_menu(event)
    
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
        self.draw_main_menu()
        self.draw_menu_options()