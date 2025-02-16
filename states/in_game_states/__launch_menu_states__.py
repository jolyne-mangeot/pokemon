import pygame as pg

class Launch_menu_states:

    def update_options(self):
        match self.menu_state:
            case "launch_fight_confirm":
                self.init_render_option_confirm()
            case "manage_team":
                self.init_render_option_team(self.player_pokedex.player_team)
                self.pre_render_team()
                self.picked_index = None
            case "save":
                self.from_top = self.screen_rect.height / 3
                self.spacer = 60
                self.init_render_option_save()
            case "save_confirm" | "quit" | "delete_save":
                self.init_render_option_confirm() # set from top, spacer and options
            case "main" | _:
                self.from_top = self.screen_rect.height / 4
                self.spacer = 60
                self.init_render_option_main()
        self.selected_index = 0
        self.pre_render_options()

    def init_render_option_main(self):
        self.menu_state = "main"
        self.options = [
            self.dialogs["launch"],
            self.dialogs["manage met pokemons"],
            self.dialogs["manage team"],
            self.dialogs["save"],
            self.dialogs["quit"]
            ]
        self.next_list = ["launch_fight_confirm", "manage_settings", "manage_team", "save", "quit"]

    def get_event_main(self, event):
        if event.type == pg.KEYDOWN:
            pressed_keys = pg.key.get_pressed()
            if pressed_keys[pg.key.key_code(self.delete_save_keys[0])] \
                and pressed_keys[pg.key.key_code(self.delete_save_keys[1])] \
                    and pressed_keys[pg.key.key_code(self.delete_save_keys[2])]:
                self.menu_state = "delete_save"
                self.update_options()
            elif pg.key.name(event.key) in self.return_keys and not self.quit:
                self.menu_state = "quit"
                self.update_options()
            elif pg.key.name(event.key) in self.confirm_keys:
                self.menu_state = self.next_list[self.selected_index]
                self.update_options()

    def get_event_manage_team(self, event):
        if event.type == pg.KEYDOWN:
            if pg.key.name(event.key) in self.return_keys and not self.quit\
                or pg.key.name(event.key) in self.confirm_keys and self.selected_index == len(self.options) - 1:
                self.menu_state = "main"
                self.update_options()
                return None
            elif pg.key.name(event.key) in self.confirm_keys:
                if type(self.picked_index) != int:
                    self.picked_index = self.selected_index
                else:
                    self.player_pokedex.switch_pokemon(self.picked_index, self.selected_index)
                    self.update_options()
                    self.picked_index = None

    def init_render_option_save(self):
        self.options = [
            self.dialogs["save_1"],
            self.dialogs["save_2"],
            self.dialogs["back"]
        ]

    def get_event_save(self, event):
        if event.type == pg.KEYDOWN:
            if pg.key.name(event.key) in self.return_keys and not self.quit\
                or pg.key.name(event.key) in self.confirm_keys and self.selected_index == 2:
                self.menu_state = "main"
                self.update_options()
                return None
            elif pg.key.name(event.key) in self.confirm_keys and self.selected_index in (0,1):
                chosen_save = str(self.selected_index + 1)
                self.menu_state = "save_confirm"
                self.update_options()
                return chosen_save
        return None

    def get_event_save_confirm(self, event):
        if event.type == pg.KEYDOWN:
            if pg.key.name(event.key) in self.return_keys and not self.quit\
                or pg.key.name(event.key) in self.confirm_keys and self.selected_index == 0:
                self.menu_state = "main"
                self.update_options()
                return None
            if pg.key.name(event.key) in self.confirm_keys and self.selected_index == 1:
                self.menu_state = "main"
                self.update_options()
                return True
    
    def get_event_delete_save(self, event):
        if event.type == pg.KEYDOWN:
            if pg.key.name(event.key) in self.return_keys and not self.quit\
                or pg.key.name(event.key) in self.confirm_keys and self.selected_index == 0:
                self.menu_state = "main"
                self.update_options()
                return None
            if pg.key.name(event.key) in self.confirm_keys and self.selected_index == 1:
                self.next = "main_menu"
                self.done = True
                self.selected_index = 0
                return True

    def get_event_launch_fight_confirm(self, event):
        if event.type == pg.KEYDOWN:
            if pg.key.name(event.key) in self.return_keys and not self.quit\
                or pg.key.name(event.key) in self.confirm_keys and self.selected_index == 0:
                self.menu_state = "main"
                self.update_options()
                return None
            if pg.key.name(event.key) in self.confirm_keys and self.selected_index == 1:
                return True