import pygame as pg

class New_game_controller:
    """
    Class responsible for handling the new game setup, including menu interactions.
    """
    def get_event(self, event):
        """
            get all pygame-related events proper to the menu before
            checking main menu shared events
        """
        if event.type == pg.QUIT:
            self.quit = True

        match self.menu_state:
            case "pokemon_choice":
                self.get_event_pokemon_choice(event)
                self.pokemon_choice.get_event_horizontal(event)
            case "player_input":
                self.get_event_player_input(event)
                self.player_input.get_event_input(event)

    def get_event_pokemon_choice(self, event):
        """
        Handles keypress events in the 'pokemon_choice' menu state
        """
        if event.type == pg.KEYDOWN:
            if pg.key.name(event.key) in self.return_keys and not self.quit:
                self.next = "title_menu"
                self.done = True
            elif pg.key.name(event.key) in self.confirm_keys:
                self.menu_effects_channel.play(self.menues_sounds["confirm"])
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
                self.menu_effects_channel.play(self.menues_sounds["confirm"])
                self.menu_state = "pokemon_choice"