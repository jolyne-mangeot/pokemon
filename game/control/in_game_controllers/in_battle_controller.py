import pygame as pg
import random

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

    def update_turn(self, game_state):
        """
        Updates the turn state and executes appropriate actions.
        """
        self.game_state = game_state
        self.animation_frame = 0
    
    def end_player_turn(self, action=None):
        if action == "guarded":
            pass
        else:
            self.battle.player_guarded = False
        if self.battle.check_active_pokemon():
            self.update_turn("enemy_beat")
        else:
            self.update_turn("enemy_turn")

    def enemy_turn_action(self):
        if random.randint(0,100) > 80 + self.battle.enemy_pokemon.level/2:
            self.update_turn("enemy_idle")
        elif random.randint(0,100) < 40 + self.battle.enemy_pokemon.level:
            self.update_turn("enemy_guard")
        else:
            self.update_turn("enemy_attack") 

    def end_enemy_turn(self, action=None):
        if action == "guarded":
            pass
        else:
            self.battle.enemy_guarded = False
        if self.battle.check_active_pokemon():
            self.update_turn("active_beat")
        else:
            self.update_options("battle_stage", True)
            self.update_turn("player_turn")

    def get_event(self, event):
        if self.game_state == "player_turn":
            self.options_states_dict[self.options_states](event)
        else:
            pass

    def get_event_battle_stage(self, event):
        """
            Handles player input in the battle stage.
        """
        if event.type == pg.KEYDOWN:
            if pg.key.name(event.key) in self.return_keys and not self.quit:
                self.update_options("run_away")

            elif pg.key.name(event.key) in self.confirm_keys and self.battle_stage_menu.selected_index == 0:
                if random.randint(0,100) > 90 + self.battle.active_pokemon.level/100:
                    self.update_turn("player_idle")
                else:
                    self.update_turn("player_attack")

            elif pg.key.name(event.key) in self.confirm_keys and self.battle_stage_menu.selected_index == 1:
                if random.randint(0,100) < 90 + self.battle.active_pokemon.level/100:
                    self.update_turn("player_idle")
                else:
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
        self.display_items_menu.get_event_chart(event)

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
            self.display_team_menu.get_event_chart(event)

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