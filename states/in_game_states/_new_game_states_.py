import pygame as pg

class New_game_states:

    def update_options(self):
        match self.menu_state:
            case "player_input":
                self.from_top = self.screen_rect.height / 2
                self.options = []
            case "pokemon_choice":
                self.from_top = self.screen_rect.height*0.7
                self.spacer = 60
                self.selected_index = 1
                self.init_render_option_pokemon_choice()
            case "quit":
                self.from_top = self.screen_rect.height/2
                self.spacer = 60
                self.selected_index = 0
                self.init_render_option_confirm()
            case "player_input":
                pass
        self.pre_render_options()

    def init_render_option_pokemon_choice(self):
        self.options = [
            self.dialogs["bulbasaur"],
            self.dialogs["charmander"],
            self.dialogs["squirtle"]
            ]

    def get_event_pokemon_choice(self, event):
        if event.type == pg.KEYDOWN:
            if pg.key.name(event.key) in self.return_keys and not self.quit:
                self.menu_state = "quit"
                self.update_options()
            elif pg.key.name(event.key) in self.confirm_keys:
                self.chosen_pokemon = "000" + str(self.selected_index*3 + 1)
                self.init_save_file()
                self.next = "launch_menu"
                self.done = True
                self.selected_index = 0