import pygame as pg

class Launch_menu_states:

    def update_options(self):
        match self.menu_state:
            case "manage_team":
                self.manage_team_menu.update_options(
                    self.init_render_option_team(self.player_pokedex.player_team)
                )
                self.manage_team_menu.pre_render()
                self.manage_team_menu.picked_index = None
            case "save":
                self.save_menu.selected_index = 0
            case "save_confirm" | "quit" | "delete_save" | "launch_fight_confirm":
                self.confirm_action_menu.selected_index = 0
            case "main_launch_menu" | _:
                self.main_launch_menu.selected_index = 0

    def get_event_main_launch_menu(self, event):
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
                self.menu_state = self.main_launch_menu.next_list[self.main_launch_menu.selected_index]
                self.update_options()
        self.main_launch_menu.get_event_vertical(event)

    def get_event_manage_team(self, event):
        if event.type == pg.KEYDOWN:
            if pg.key.name(event.key) in self.return_keys and not self.quit\
                or pg.key.name(event.key) in self.confirm_keys and self.manage_team_menu.selected_index == len(self.manage_team_menu.options) - 1:
                self.menu_state = "main_launch_menu"
                self.update_options()
                return None
            elif pg.key.name(event.key) in self.confirm_keys:
                if type(self.manage_team_menu.picked_index) != int:
                    self.manage_team_menu.picked_index = self.manage_team_menu.selected_index
                else:
                    self.player_pokedex.switch_pokemon(self.manage_team_menu.picked_index, self.manage_team_menu.selected_index)
                    self.update_options()
                    self.manage_team_menu.picked_index = None
        self.manage_team_menu.get_event_vertical(event)

    def get_event_save(self, event):
        if event.type == pg.KEYDOWN:
            if pg.key.name(event.key) in self.return_keys and not self.quit\
                or pg.key.name(event.key) in self.confirm_keys and self.save_menu.selected_index == 2:
                self.menu_state = "main_launch_menu"
                self.update_options()
            elif pg.key.name(event.key) in self.confirm_keys and self.save_menu.selected_index in (0,1):
                self.menu_state = "save_confirm"
                self.update_options()
        self.save_menu.get_event_vertical(event)

    def get_event_save_confirm(self, event):
        if event.type == pg.KEYDOWN:
            if pg.key.name(event.key) in self.return_keys and not self.quit\
                or pg.key.name(event.key) in self.confirm_keys and self.confirm_action_menu.selected_index == 0:
                self.menu_state = "main_launch_menu"
                self.update_options()
                return None
            if pg.key.name(event.key) in self.confirm_keys and self.confirm_action_menu.selected_index == 1:
                self.menu_state = "main_launch_menu"
                self.update_options()
                return True
        self.confirm_action_menu.get_event_vertical(event)
    
    def get_event_delete_save(self, event):
        if event.type == pg.KEYDOWN:
            if pg.key.name(event.key) in self.return_keys and not self.quit\
                or pg.key.name(event.key) in self.confirm_keys and self.confirm_action_menu.selected_index == 0:
                self.menu_state = "main_launch_menu"
                self.update_options()
                return None
            if pg.key.name(event.key) in self.confirm_keys and self.confirm_action_menu.selected_index == 1:
                self.next = "main_menu"
                self.done = True
                return True
        self.confirm_action_menu.get_event_vertical(event)

    def get_event_launch_fight_confirm(self, event):
        if event.type == pg.KEYDOWN:
            if pg.key.name(event.key) in self.return_keys and not self.quit\
                or pg.key.name(event.key) in self.confirm_keys and self.confirm_action_menu.selected_index == 0:
                self.menu_state = "main_launch_menu"
                self.update_options()
                return None
            if pg.key.name(event.key) in self.confirm_keys and self.confirm_action_menu.selected_index == 1:
                return True
        self.confirm_action_menu.get_event_vertical(event)
        
    def get_event_quit(self, event):
        if event.type == pg.KEYDOWN:
            if pg.key.name(event.key) in self.return_keys and not self.quit or\
                pg.key.name(event.key) in self.confirm_keys and self.confirm_action_menu.selected_index == 0:
                self.menu_state = "main_launch_menu"
                self.update_options()
            elif pg.key.name(event.key) in self.confirm_keys and self.confirm_action_menu.selected_index == 1:
                self.next = "main_menu"
                self.done = True
        self.confirm_action_menu.get_event_vertical(event)