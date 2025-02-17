import pygame as pg

class In_battle_controller:

    def update_options(self):
        match self.menu_state:
            case "display_items":
                self.display_items_menu.selected_index = 0
            case "display_team":
                self.display_team_menu.update_options(
                    self.init_render_option_team(self.battle.player_team, self.forced_switch, self.team_full)
                )
                self.display_team_menu.selected_index = 0
                self.picked_index = None
            case "select_pokemon_confirm":
                self.confirm_action_menu.selected_index = 0
            case "run_away":
                self.confirm_action_menu.selected_index = 0
            case "battle_stage" | _:
                self.battle_stage_menu.selected_index = 0

    def get_event_battle_stage(self, event):
        if event.type == pg.KEYDOWN:
            if pg.key.name(event.key) in self.return_keys and not self.quit:
                self.menu_state = "run_away"
                self.update_options()
            elif pg.key.name(event.key) in self.confirm_keys and self.battle_stage_menu.selected_index == 0:
                self.battle.attack(True, self.enemy_guarded)
                if self.update_battle_status() != "switch":
                    self.enemy_turn = True
                    self.enemy_guarded = False
            elif pg.key.name(event.key) in self.confirm_keys and self.battle_stage_menu.selected_index == 1:
                self.guarded = True
                self.enemy_turn = True
                self.enemy_guarded = False
            elif pg.key.name(event.key) in self.confirm_keys and self.battle_stage_menu.selected_index in (2,3,4):
                self.menu_state = self.battle_stage_menu.next_list[self.battle_stage_menu.selected_index]
                self.update_options()
        self.battle_stage_menu.get_event_vertical(event)
    
    def get_event_display_items(self, event):
        if event.type == pg.KEYDOWN:
            if pg.key.name(event.key) in self.return_keys and not self.quit\
                or pg.key.name(event.key) in self.confirm_keys and self.display_items_menu.selected_index == len(self.display_items_menu.options) - 1:
                self.menu_state = "battle_stage"
                self.update_options()
            elif pg.key.name(event.key) in self.confirm_keys and self.display_items_menu.selected_index == 0:
                if self.battle.wild:
                    self.caught = self.battle.catch_attempt()
                    self.menu_state = "battle_stage"
                    self.update_options()
                    if not self.caught:
                        self.enemy_turn = True
        self.display_items_menu.get_event_vertical(event)

    def get_event_display_team(self, event):
        if event.type == pg.KEYDOWN:
            if pg.key.name(event.key) in self.return_keys and not self.quit and not self.forced_switch\
                or pg.key.name(event.key) in self.confirm_keys and self.display_team_menu.selected_index == len(self.display_team_menu.options) - 1\
                    and not self.forced_switch and not self.team_full:
                self.menu_state = "battle_stage"
                self.update_options()
            elif pg.key.name(event.key) in self.confirm_keys:
                if self.display_team_menu.selected_index == self.battle.player_team.index(self.battle.active_pokemon) and self.team_full:
                    self.chosen_pokemon = self.display_team_menu.selected_index
                    self.menu_state = "select_pokemon_confirm"
                    self.update_options()
                elif self.display_team_menu.selected_index == self.battle.player_team.index(self.battle.active_pokemon) or\
                    self.battle.player_team[self.display_team_menu.selected_index].current_health_points <= 0:
                    pass
                else:
                    self.chosen_pokemon = self.display_team_menu.selected_index
                    self.menu_state = "select_pokemon_confirm"
                    self.update_options()
        self.display_team_menu.get_event_vertical(event)
    
    def get_event_run_away(self, event):
        if event.type == pg.KEYDOWN:
            if pg.key.name(event.key) in self.return_keys and not self.quit\
                or pg.key.name(event.key) in self.confirm_keys and self.confirm_action_menu.selected_index == 0:
                self.menu_state = "battle_stage"
                self.update_options()
            if pg.key.name(event.key) in self.confirm_keys and self.confirm_action_menu.selected_index == 1:
                if self.battle.run_away():
                    self.next = "launch_menu"
                    self.done = True
                else:
                    self.menu_state = "battle_stage"
                    self.update_options()
                    self.enemy_turn = True
        self.confirm_action_menu.get_event_vertical(event)

    def get_event_select_pokemon_confirm(self, event):
        if event.type == pg.KEYDOWN:
            if pg.key.name(event.key) in self.return_keys and not self.quit\
                or pg.key.name(event.key) in self.confirm_keys and self.confirm_action_menu.selected_index == 0:
                self.menu_state = "display_team"
                self.update_options()
                return None
            if pg.key.name(event.key) in self.confirm_keys and self.confirm_action_menu.selected_index == 1:
                self.menu_state = "battle_stage"
                self.update_options()
                return True
        self.confirm_action_menu.get_event_vertical(event)