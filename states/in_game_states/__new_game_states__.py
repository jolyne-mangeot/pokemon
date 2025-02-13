import pygame as pg

class Launch_menu_states:

    def update_options(self, back = None):
        match self.menu_state:
            case "player_input":
                self.from_top = self.screen_rect.height / 3
                self.spacer = 60
                self.init_render_option_main()
            case "pokemon_choice":
                self.from_top = self.screen_rect.height*0.7
                self.spacer = 60
                self.init_render_option_pokemon_choice()
            case "quit":
                self.from_top = self.screen_rect.height/2
                self.spacer = 60
                self.init_render_option_confirm()
            case "player_input":
                pass
        self.selected_index = 0
        self.pre_render_options()

    # def init_render_option_main(self):
    #     pass

    # def get_event_main(self, event):
    #         if pg.key.name(event.key) in self.return_keys and not self.quit:
    #             self.menu_state = "quit"
    #             self.update_options()

    def init_render_option_pokemon_choice(self):
        pass

    def get_event_pokemon_choice(self, event):
            if pg.key.name(event.key) in self.return_keys and not self.quit:
                self.menu_state = "quit"
                self.update_options()