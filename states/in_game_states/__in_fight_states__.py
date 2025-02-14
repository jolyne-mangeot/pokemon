import pygame as pg

class In_fight_states:

    def update_options(self):
        match self.menu_state:
            case "display_item":
                self.init_render_option_confirm()
            case "display_team":
                self.init_render_option_team(self.fight.player_team)
                self.pre_render_team()
                self.picked_index = None
            case "select_pokemon_confirm":
                self.init_render_option_confirm()
            case "quit":
                self.init_render_option_confirm()
            case "battle_stage" | _:
                self.from_top = self.screen_rect.height / 4
                self.spacer = 60
                self.init_render_option_battle_stage()
        self.selected_index = 0
        self.pre_render_options()

    def init_render_option_battle_stage(self):
        self.menu_state = "battle_stage"
        self.options = [
            self.dialogs["attack"],
            self.dialogs["guard"],
            self.dialogs["team"],
            self.dialogs["items"],
            self.dialogs["run away"]
            ]
        self.next_list = ["", "", "display_team", "display_items", "quit"]

    def get_event_battle_stage(self, event):
        if event.type == pg.KEYDOWN:
            if pg.key.name(event.key) in self.return_keys and not self.quit:
                self.menu_state = "quit"
                self.update_options()
            elif pg.key.name(event.key) in self.confirm_keys and self.selected_index == 0:
                self.fight.attack(True)
                self.enemy_turn = True
            elif pg.key.name(event.key) in self.confirm_keys and self.selected_index == 1:
                self.guarded = True
                self.enemy_turn = True
            elif pg.key.name(event.key) in self.confirm_keys and self.selected_index in (2,3,4):
                self.menu_state = self.next_list[self.selected_index]
                self.update_options()

    def get_event_display_team(self, event):
        if event.type == pg.KEYDOWN:
            if pg.key.name(event.key) in self.return_keys and not self.quit\
                or pg.key.name(event.key) in self.confirm_keys and self.selected_index == len(self.options) - 1:
                self.menu_state = "battle_stage"
                self.update_options()
            elif pg.key.name(event.key) in self.confirm_keys:
                if self.selected_index == self.fight.player_team.index(self.fight.active_pokemon):
                    pass
                else:
                    self.chosen_pokemon = self.selected_index
                    self.menu_state = "select_pokemon_confirm"
                    self.update_options()
    
    def get_event_run_away(self, event):
        if event.type == pg.KEYDOWN:
            if pg.key.name(event.key) in self.return_keys and not self.quit\
                or pg.key.name(event.key) in self.confirm_keys and self.selected_index == 0:
                self.menu_state = self.back
                self.update_options()
            if pg.key.name(event.key) in self.confirm_keys and self.selected_index == 1:
                if self.fight.run_away():
                    self.next = "launch_menu"
                    self.done = True
                    self.selected_index = 0
                else:
                    self.menu_state = "battle_stage"
                    self.update_options()

    def get_event_select_pokemon_confirm(self, event):
        if event.type == pg.KEYDOWN:
            if pg.key.name(event.key) in self.return_keys and not self.quit\
                or pg.key.name(event.key) in self.confirm_keys and self.selected_index == 0:
                self.menu_state = "display_team"
                self.update_options()
                return None
            if pg.key.name(event.key) in self.confirm_keys and self.selected_index == 1:
                self.menu_state = "in_fight"
                self.update_options()
                return True

    def draw_pokemons_infos(self):
        player_pokemon_name = self.pixel_font.render(self.fight.active_pokemon.name, 1, (0,0,0))
        player_pokemon_name_rect = player_pokemon_name.get_rect(bottomleft=(self.screen_rect.width*0.58,self.screen_rect.height*0.62))
    
        enemy_pokemon_name = self.pixel_font.render(self.fight.enemy_pokemon.name, 1, (0,0,0))
        enemy_pokemon_name_rect = enemy_pokemon_name.get_rect(bottomleft=(self.screen_rect.width*0.05, self.screen_rect.height*0.08))

        self.screen.blit(player_pokemon_name, player_pokemon_name_rect)
        self.screen.blit(enemy_pokemon_name, enemy_pokemon_name_rect)
    
    def draw_pokemons_health_points(self):
        player_pokemon_bar_rect = (self.screen_rect.width*0.65, self.screen_rect.height*0.65, 200, 20)
        player_pokemon_health_rect = (self.screen_rect.width*0.65, self.screen_rect.height*0.65,\
                    self.fight.active_pokemon.current_health_points / self.fight.active_pokemon.health_points *200, 20)
        pg.draw.rect(self.screen, (255,0,0), player_pokemon_bar_rect)
        pg.draw.rect(self.screen, (0,255,0), player_pokemon_health_rect)

        enemy_pokemon_bar_rect = (self.screen_rect.width*0.15, self.screen_rect.height*0.1, 200, 20)
        enemy_pokemon_health_rect = (self.screen_rect.width*0.15, self.screen_rect.height*0.1,\
                    self.fight.enemy_pokemon.current_health_points / self.fight.enemy_pokemon.health_points *200, 20)
        pg.draw.rect(self.screen, (255,0,0), enemy_pokemon_bar_rect)
        pg.draw.rect(self.screen, (0,255,0), enemy_pokemon_health_rect)