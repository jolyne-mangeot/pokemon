import pygame as pg

from game.control.models_controller import Models_controller
from game.views.main_menu_views.main_menues_display import Main_menues_display
from game.views.main_menu_views.main_menues_sounds import Main_menues_sounds

from game.models.pokemons.pokedex import Pokedex

class Load_menu(
    Models_controller, 
    Main_menues_display, Main_menues_sounds):

    def __init__(self):
        """
            inits values specific to the menu such as navigation and
            placement of options
        """
        Models_controller.__init__(self)
        self.init_config()
        self.init_main_menu_display()
        self.init_main_menues_sounds()

    def startup(self):
        """
            initiates all menu-related data
        """
        self.player_saves_state = self.load_player_data()
        self.init_load_menu_object()

    def update(self):
        """
            trigger all changes such as mouse hover or changing selected
            option, done after having checked in control class change on
            done and quit attribute from menu_manager inheritance
        """
        self.draw()

    def cleanup(self):
        """
            cleans up all menu related data
        """
        pass

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
            if pg.key.name(event.key) in self.return_keys and not self.quit:
                self.menu_effects_channel.play(self.menues_sounds["back"])
                self.next = "title_menu"
                self.done = True

            elif pg.key.name(event.key) in self.confirm_keys and\
                    self.load_menu.selected_index == len(
                        self.load_menu.next_list) - 1:
                self.menu_effects_channel.play(self.menues_sounds["confirm"])
                self.next = "title_menu"
                self.done = True

            elif pg.key.name(event.key) in self.confirm_keys:
                self.menu_effects_channel.play(self.menues_sounds["confirm"])
                if self.load_menu.next_list[self.load_menu.selected_index] == "new_game":
                    self.music_channel.stop()
                    self.select_option(self.load_menu)
                else:
                    self.music_channel.stop()
                    self.init_player_save()
                    self.select_option(self.load_menu)

        self.load_menu.get_event_vertical(event)

    def select_option(self, menu):
        """
            change the active state with done attribute and change it
            to correct user input
        """
        self.next = menu.next_list[menu.selected_index]
        self.done = True

    def draw(self):
        """
            init all display related script
        """
        self.draw_load_screen()
        self.blit_dialog(self.dialogs["save select"], self.width*0.032,self.width*0.5,self.height*0.2,"midbottom", (0,0,0),True)
        self.load_menu.draw_vertical_options()