import pygame as pg

class New_game_controller:

    def update_options(self):
        match self.menu_state:
            case "player_input":
                pass
            case "pokemon_choice":
                pass

    def get_event_pokemon_choice(self, event):
        if event.type == pg.KEYDOWN:
            if pg.key.name(event.key) in self.return_keys and not self.quit:
                self.next = "title_menu"
                self.done = True
            elif pg.key.name(event.key) in self.confirm_keys:
                self.init_save_file()
                self.next = "launch_menu"
                self.done = True
    
    def get_event_player_input(self, event):
        if event.type == pg.KEYDOWN:
            if pg.key.name(event.key) in self.return_keys:
                self.next = "title_menu"
                self.done = True
            elif pg.key.name(event.key) in self.confirm_keys and self.player_input != "":
                self.menu_state = "pokemon_choice"
                self.update_options()