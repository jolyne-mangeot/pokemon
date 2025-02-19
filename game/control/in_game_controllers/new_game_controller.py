import pygame as pg

class New_game_controller:
    """
    Class responsible for handling the new game setup, including menu interactions.
    """

    def update_options(self):
        """
        Updates menu options based on the current menu state.
        """
        match self.menu_state:
            case "player_input":
                pass
            case "pokemon_choice":
                pass

    def get_event_pokemon_choice(self, event):
        """
        Handles keypress events in the 'pokemon_choice' menu state
        """
        if event.type == pg.KEYDOWN:
            if pg.key.name(event.key) in self.return_keys and not self.quit:
                self.next = "title_menu"
                self.done = True
            elif pg.key.name(event.key) in self.confirm_keys:
                self.init_save_file()
                self.next = "launch_menu"
                self.done = True
    
    def get_event_player_input(self, event):
        """
        Handles keypress events in the 'player_input' menu state.
        """
        if event.type == pg.KEYDOWN:
            if pg.key.name(event.key) in self.return_keys:
                self.next = "title_menu"
                self.done = True
            elif pg.key.name(event.key) in self.confirm_keys and self.player_input != "":
                self.menu_state = "pokemon_choice"
                self.update_options()