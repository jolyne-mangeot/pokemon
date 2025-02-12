import pygame as pg

class Pause_menu_save_quit:
    def init_render_option_save(self):
        self.options = ["save_file_1", "save_file_2", self.dialogs["back"]]
    
    def init_render_option_save_confirm(self):
        self.options = ["no", "yes"]
    
    def init_render_option_quit(self):
        self.options = ["no", "yes"]
        self.next_list = ["", "main_menu"]
    
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

    def get_event_quit(self, event):
        if event.type == pg.KEYDOWN:
            if pg.key.name(event.key) in self.return_keys and not self.quit or\
                pg.key.name(event.key) in self.confirm_keys and self.selected_index == 0:
                self.menu_state = "main"
                self.update_options()