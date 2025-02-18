import pygame as pg

class In_battle_controller:

    def update_options(self, options_states, player_turn_start=False):
        self.options_states = options_states
        match self.options_states:
            case "battle_stage":
                if player_turn_start:
                    self.battle_stage_menu.selected_index = 0
            case "display_items":
                self.display_items_menu.selected_index = 0
            case "display_team":
                self.display_team_menu.selected_index = 0
                self.display_team_menu.update_options(
                    self.init_render_option_team(self.battle.player_team, self.forced_switch, self.team_full)
                )
            case "select_pokemon_confirm":
                self.chosen_pokemon = self.display_team_menu.selected_index
                self.confirm_action_menu.selected_index = 0
            case "run_away":
                self.confirm_action_menu.selected_index = 0
    
    def end_player_turn(self, action=None):
        if action == "guarded":
            pass
        else:
            self.battle.player_guarded = False
        if not self.ran_away and not self.caught:
            self.game_state = "enemy_turn"
        self.update_battle_status()
    
    def end_enemy_turn(self, action=None):
        if action == "guarded":
            pass
        else:
            self.battle.enemy_guarded = False
        self.update_options("battle_stage", True)
        self.game_state = "player_turn"
        self.update_battle_status()

    def update_turn(self, game_state):
        self.game_state = game_state

        match self.game_state:
            case "player_attack":
                self.animation_frame = 0
            case "player_guard":
                self.battle.guard(True)
                self.animation_frame = 0

            case "enemy_attack":
                self.animation_frame = 0
            case "enemy_guard":
                self.battle.guard(False)
                self.animation_frame = 0

            case "catch_attempt":
                if self.battle.wild:
                    self.caught = self.battle.catch_attempt()
                    self.update_options("battle_stage")
                    if self.caught:
                        self.battle.player_pokedex.catch_pokemon(
                            self.battle.enemy_pokemon.entry, 
                            self.battle.enemy_pokemon.experience_points
                        )
                        self.end_player_turn()
                    else:
                        self.end_player_turn()
                
            case "switch_pokemon_confirmed":
                if self.team_full:
                    self.battle.player_team.pop(self.chosen_pokemon)
                    self.update_battle_status()
                else:
                    self.battle.spawn_pokemon(self.chosen_pokemon, True)
                    self.forced_switch = False
                    self.end_player_turn()

            case "run_away_attempt":
                if self.battle.run_away():
                    self.ran_away = True
                    self.end_player_turn()
                else:
                    self.update_options("battle_stage")
                    self.end_player_turn()


    def get_event_battle_stage(self, event):
        if event.type == pg.KEYDOWN:
            if pg.key.name(event.key) in self.return_keys and not self.quit:
                self.update_options("run_away")

            elif pg.key.name(event.key) in self.confirm_keys and self.battle_stage_menu.selected_index == 0:
                self.update_turn("player_attack")

            elif pg.key.name(event.key) in self.confirm_keys and self.battle_stage_menu.selected_index == 1:
                self.update_turn("player_guard")

            elif pg.key.name(event.key) in self.confirm_keys and self.battle_stage_menu.selected_index in (2,3,4):
                self.update_options(self.battle_stage_menu.next_list[self.battle_stage_menu.selected_index])
        self.battle_stage_menu.get_event_vertical(event)


    def get_event_display_items(self, event):
        if event.type == pg.KEYDOWN:
            if pg.key.name(event.key) in self.return_keys and not self.quit\
                or pg.key.name(event.key) in self.confirm_keys and self.display_items_menu.selected_index == len(self.display_items_menu.options) - 1:
                self.update_options("battle_stage")

            elif pg.key.name(event.key) in self.confirm_keys and self.display_items_menu.selected_index == 0:
                self.update_turn("catch_attempt")
        self.display_items_menu.get_event_vertical(event)


    def get_event_display_team(self, event):
        if event.type == pg.KEYDOWN:
            if pg.key.name(event.key) in self.return_keys:
                if not self.quit and not self.forced_switch and not self.team_full:
                    self.update_options("battle_stage")

            elif pg.key.name(event.key) in self.confirm_keys:
                if pg.key.name(event.key) in self.confirm_keys and\
                        self.display_team_menu.selected_index == len(self.display_team_menu.options) - 1\
                        and not self.forced_switch and not self.team_full:
                    self.update_options("battle_stage")

                elif self.display_team_menu.selected_index == self.battle.player_team.index(self.battle.active_pokemon)\
                        and not self.team_full or\
                        self.battle.player_team[self.display_team_menu.selected_index].current_health_points <= 0 and not self.team_full:
                    pass
                else:
                    self.update_options("select_pokemon_confirm")
        self.display_team_menu.get_event_vertical(event)


    def get_event_select_pokemon_confirm(self, event):
        if event.type == pg.KEYDOWN:
            if pg.key.name(event.key) in self.return_keys and not self.quit\
                or pg.key.name(event.key) in self.confirm_keys and self.confirm_action_menu.selected_index == 0:
                self.update_options("display_team")

            if pg.key.name(event.key) in self.confirm_keys and self.confirm_action_menu.selected_index == 1:
                self.update_turn("switch_pokemon_confirmed")
        self.confirm_action_menu.get_event_vertical(event)


    def get_event_run_away(self, event):
        if event.type == pg.KEYDOWN:
            if pg.key.name(event.key) in self.return_keys and not self.quit\
                    or pg.key.name(event.key) in self.confirm_keys and self.confirm_action_menu.selected_index == 0:
                self.update_options("battle_stage")

            if pg.key.name(event.key) in self.confirm_keys and self.confirm_action_menu.selected_index == 1:
                self.update_turn("run_away_attempt")
        self.confirm_action_menu.get_event_vertical(event)