import pygame as pg

class Launch_menu_states:
    def init_render_option_main(self):
        self.menu_state = "main"
        self.options = ["launch", "manage team", "manage met pokemons", "save", "quit"]
        self.next_list = ["in_fight", "manage_settings", "manage_settings", "save", "quit"]

    def get_event_main(self, event):
        if event.type == pg.KEYDOWN:
            if pg.key.name(event.key) in self.return_keys and not self.quit:
                self.menu_state = "quit"
                self.update_options()
            if pg.key.name(event.key) in self.confirm_keys and self.selected_index in (3,4):
                self.menu_state = self.next_list[self.selected_index]
                self.update_options()

    def init_render_option_manage_team(self):
        self.menu_state = "manage_team"
        self.options = ["pokemon1", "pokemon2", self.dialogs["back"]]
        self.next_list = ["", "", "pause_menu"]

    def init_render_option_save(self):
        self.options = ["save_file_1", "save_file_2", self.dialogs["back"]]

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

    def init_render_option_confirm(self):
        self.options = ["no", "yes"]

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

    def get_event_quit(self, event):
        if event.type == pg.KEYDOWN:
            if pg.key.name(event.key) in self.return_keys and not self.quit or\
                pg.key.name(event.key) in self.confirm_keys and self.selected_index == 0:
                self.menu_state = "main"
                self.update_options()
            elif pg.key.name(event.key) in self.confirm_keys and self.selected_index == 1:
                self.next = "main_menu"
                self.done = True
                self.selected_index = 0