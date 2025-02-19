import pygame as pg

class In_battle_controller:
    """
    Controls the battle system, including turn-based mechanics, menu navigation, 
    and interaction handling for a Pokémon-style game.
    """

    def update_options(self, options_states, player_turn_start=False):
        """
        Updates battle menu options depending on the game state.
        """
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
                self.confirm_action_menu.selected_index = 1
            case "run_away":
                self.confirm_action_menu.selected_index = 1
    
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
        """
        Updates the turn state and executes appropriate actions.
        """
        self.game_state = game_state
        self.animation_frame = 0

        match self.game_state:
            case "player_attack":
                self.animation_frame = 0
            case "player_guard":
                
                self.animation_frame = 0

            case "enemy_attack":
                self.animation_frame = 0
            case "enemy_guard":
                
                self.animation_frame = 0

            case "catch_attempt":
                pass
                
            case "switch_pokemon_confirmed":
                pass

            case "run_away_attempt":
                if self.battle.run_away():
                    self.ran_away = True
                    self.end_player_turn()
                else:
                    self.update_options("battle_stage")
                    self.end_player_turn()

    def start_game_scene(self, none=None):
        """
        Handles player input in the battle stage.
        """
        if not self.enemy_spawn_animation_done:
            if self.animate_spawn(False, False):
                self.play_enemy_pokemon_cry()
                self.enemy_spawn_animation_done = True
                self.animation_frame = 0
            else:
                self.animation_frame +=1
        elif not self.player_spawn_animation_done:
            if self.animate_spawn(True, True):
                self.in_game_actions_sounds["pokemon out"].play()
                self.play_active_pokemon_cry()
                self.player_spawn_animation_done = True
                self.animation_frame = 0
            else:
                self.animation_frame +=1
        else:
            self.end_enemy_turn()
    
    def pokemon_attack_scene(self, attacker="player_attack"):
        if attacker == "player_attack":
            if self.animate_attack(True):
                self.end_player_turn()
            else:
                self.animation_frame +=1
                if self.animation_frame == 60:
                    self.efficiency = self.battle.attack(True)
                    if self.efficiency >= 2:
                        self.in_game_actions_sounds["hit very effective"].play()
                    elif self.efficiency >=0.5:
                        self.in_game_actions_sounds["hit not very effective"].play()
                    else:
                        self.in_game_actions_sounds["hit non effective"].play()
        else:
            if self.animate_attack(False):
                self.end_enemy_turn()
            else:
                self.animation_frame +=1
                if self.animation_frame == 60:
                    self.efficiency = self.battle.attack(False)
                    if self.efficiency >= 2:
                        self.in_game_actions_sounds["hit very effective"].play()
                    elif self.efficiency >=0.5:
                        self.in_game_actions_sounds["hit not very effective"].play()
                    else:
                        self.in_game_actions_sounds["hit non effective"].play()
    
    def pokemon_guard_scene(self, guarding="player_guard"):
        if guarding == "player_guard":
            self.battle.guard(True)
            if self.animate_guard(True):
                self.end_player_turn("guarded")
            else:
                self.animation_frame += 1
        else:
            self.battle.guard(False)
            if self.animate_guard(False):
                self.end_enemy_turn("guarded")
            else:
                self.animation_frame += 1
    
    def pokemon_switch_scene(self, none=None):
        if self.team_full:
            self.battle.player_team.pop(self.chosen_pokemon)
            self.update_battle_status()
        else:
            if not self.remove_animation_done:
                if self.forced_switch or self.animate_remove():
                    self.battle.spawn_pokemon(self.chosen_pokemon, True)
                    self.in_game_actions_sounds["pokemon out"].play()
                    self.play_active_pokemon_cry()
                    self.remove_animation_done = True
                    self.animation_frame = 0
                else:
                    self.animation_frame +=1
            elif self.animate_spawn(True, True, True):
                if self.forced_switch:
                    self.update_options("battle_stage")
                    self.game_state = "player_turn"
                else:
                    self.end_player_turn()
                self.forced_switch = False
                self.remove_animation_done = False
            else:
                self.animation_frame +=1
    
    def pokemon_beat_scene(self, beat="active_beat"):
        if beat == "active_beat":
            if self.animate_beat(True):
                self.beat_animation_done = True
                self.update_battle_status()
            else:
                self.animation_frame +=1
        else:
            if self.animate_beat(False):
                self.beat_animation_done = True
                self.update_battle_status()
            else:
                self.animation_frame +=1
    
    def catch_attempt_scene(self, none=None):
        if self.animation_frame == 150 and self.battle.wild:
            self.caught = self.battle.catch_attempt()
            if self.caught:
                self.in_battle_musics["caught pokemon"].play()
        if self.animate_catch_attempt():
            if not self.battle.wild:
                self.game_state = "player_turn"
            else:
                if self.caught:
                    self.battle.player_pokedex.catch_pokemon(
                        self.battle.enemy_pokemon.entry, 
                        self.battle.enemy_pokemon.experience_points
                    )
                    self.update_battle_status()
                else:
                    self.end_player_turn()
        else:
            self.animation_frame +=1

    def get_event_battle_stage(self, event):
        """
            Handles player input in the battle stage.
        """
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
        """
            Handles player input in the item menu.
        """
        if event.type == pg.KEYDOWN:
            if pg.key.name(event.key) in self.return_keys and not self.quit\
                or pg.key.name(event.key) in self.confirm_keys and self.display_items_menu.selected_index == len(self.display_items_menu.options) - 1:
                self.update_options("battle_stage")

            elif pg.key.name(event.key) in self.confirm_keys and self.display_items_menu.selected_index == 0:
                self.update_turn("catch_attempt")
        self.display_items_menu.get_event_vertical(event)


    def get_event_display_team(self, event):
            """
                Handles player input in the team selection menu.
            """
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
        """
            Handles player input when confirming Pokémon selection.
        """
        if event.type == pg.KEYDOWN:
            if pg.key.name(event.key) in self.return_keys and not self.quit\
                or pg.key.name(event.key) in self.confirm_keys and self.confirm_action_menu.selected_index == 1:
                self.update_options("display_team")

            if pg.key.name(event.key) in self.confirm_keys and self.confirm_action_menu.selected_index == 0:
                self.update_turn("switch_pokemon_confirmed")
        self.confirm_action_menu.get_event_vertical(event)


    def get_event_run_away(self, event):
        """
            Handles player input when attempting to run away from battle.
        """
        if event.type == pg.KEYDOWN:
            if pg.key.name(event.key) in self.return_keys and not self.quit\
                    or pg.key.name(event.key) in self.confirm_keys and self.confirm_action_menu.selected_index == 1:
                self.update_options("battle_stage")

            if pg.key.name(event.key) in self.confirm_keys and self.confirm_action_menu.selected_index == 0:
                self.update_turn("run_away_attempt")
        self.confirm_action_menu.get_event_vertical(event)