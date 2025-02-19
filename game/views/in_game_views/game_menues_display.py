import pygame as pg

from game.views.display import Display

class Game_menues_display(Display):
    def display_init(self):
        Display.__init__(self)

    def init_in_game_display(self):
        Display.__init__(self)
        self.init_root_variables_in_game()
        self.load_graphics_launch_menues()
        self.load_graphics_pokemons()

    def init_root_variables_in_game(self):
        self.active_pokemon_image_size : tuple = (self.width*0.3, self.width*0.3)
        self.mini_image_size : tuple = (self.width*0.21, self.width*0.2)

    def load_graphics_pokemons(self):
        for pokemon in self.player_pokedex.player_team:
            back_image = pg.image.load(self.GRAPHICS_PATH + "pokemon/" + pokemon.entry + "/back.png")
            pokemon.back_image = pg.transform.scale(back_image, self.active_pokemon_image_size)
            mini_image = pg.image.load(self.GRAPHICS_PATH + "pokemon/" + pokemon.entry + "/mini.png")
            pokemon.mini_image = pg.transform.scale(mini_image, self.mini_image_size)

    def init_render_option_team(self, team, forced_switch=False, team_full=False, menu="in_battle"):
        options = []
        for pokemon in team:
            options.append(self.dialogs[pokemon.name])
            level_display = self.dialogs["lvl"] + str(int(pokemon.level))
            while len(options[-1]) + len(level_display) < (25 if menu == "launch_menu" else 16):
                options[-1] += " "
            options[-1] += level_display

        while len(options) < 6:
            options.append("")
        if not forced_switch and not team_full:
            options.append(self.dialogs['back'])
        return options
    
    def load_graphics_combat(self):
        self.pokemon_ground_img=pg.image.load(self.GRAPHICS_PATH+"/media/"+"battle_"+self.battle.battle_biome["name"]+"_ground.png")
        self.pokemon_ground_img=pg.transform.scale(self.pokemon_ground_img, (self.width*0.31,self.width*0.116))
        self.active_pokemon_ground_img=pg.transform.scale(self.pokemon_ground_img, (self.width*0.523,self.width*0.196))

        self.pokeball_img=pg.image.load(self.GRAPHICS_PATH+"/media/"+"pokeball_sprite.png")
        self.pokeball_img=pg.transform.scale(self.pokeball_img, (self.width*0.02, self.width*0.02))

        self.pokeball_caught_img=pg.image.load(self.GRAPHICS_PATH+"/media/"+"pokeball_sprite_caught.png")
        self.pokeball_caught_img=pg.transform.scale(self.pokeball_caught_img, (self.width*0.02, self.width*0.02))

        self.text_box_empty=pg.image.load(self.GRAPHICS_PATH+"/media/"+"textbox pre combat.png")
        self.text_box_empty=pg.transform.scale(self.text_box_empty, (self.width,self.height*0.35))

        self.action_bg_img=pg.image.load(self.GRAPHICS_PATH+"/media/"+"pkmn choice bg.png")
        self.action_bg_img=pg.transform.scale(self.action_bg_img,(self.width,self.height))

        self.action_box=pg.image.load(self.GRAPHICS_PATH+"/media/"+"textbox_combat.png")
        self.action_box=pg.transform.scale(self.action_box,(self.width, self.height*0.35))

        
    def load_pkmn_info_box(self):
        self.pkmn_info_box_enemy=pg.image.load(self.GRAPHICS_PATH+"/media/"+"pkmn info enemy.png")
        self.pkmn_info_box_enemy=pg.transform.scale(self.pkmn_info_box_enemy,(self.width*0.47,self.height*0.23))

        self.pkmn_info_box_player=pg.image.load(self.GRAPHICS_PATH+"/media/"+"pkmn info player.png")
        self.pkmn_info_box_player=pg.transform.scale(self.pkmn_info_box_player,(self.width*0.47,self.height*0.23))

        self.action_box=pg.image.load(self.GRAPHICS_PATH+"/media/"+"textbox_combat.png")
        self.action_box=pg.transform.scale(self.action_box,(self.width, self.height*0.35))


    def load_graphics_launch_menues(self):
        self.launch_menu_img=pg.image.load(self.GRAPHICS_PATH+"/media/"+"launch screen.png")
        self.launch_menu_img=pg.transform.scale(self.launch_menu_img, (self.width,self.height))

        self.pkmn_frame_img=pg.image.load(self.GRAPHICS_PATH+"/media/"+"pkmn frame.png")
        self.pkmn_frame_img=pg.transform.scale(self.pkmn_frame_img, (self.width*0.2, self.width*0.2))


        self.action_bg_img=pg.image.load(self.GRAPHICS_PATH+"/media/"+"pkmn choice bg.png")
        self.action_bg_img=pg.transform.scale(self.action_bg_img,(self.width,self.height))


        #########↑load, system,etc.#######↓draw##
    def draw_launch_menu(self):
        self.screen.blit(self.launch_menu_img,(0,0))
    
    def draw_pkmn_frame(self,x:int, y:int):
        self.screen.blit(self.pkmn_frame_img,(x,y))
    
    def draw_team_select_img(self):
        self.team_select_img=pg.transform.scale(self.team_select_img, (self.width,self.height))
        self.screen.blit(self.team_select_img,(0,0))
        
    def draw_action_background(self):
        self.screen.blit(self.action_bg_img,(0,0))
    
    def draw_pokeball_thrown(self):
        self.screen.blit(self.pokeball_img, (self.width*0.716, self.height*0.268))
    
    def draw_pokeball_caught(self):
        self.screen.blit(self.pokeball_caught_img, (self.width*0.72, self.height*0.26))

    def draw_dialogue_box(self):
        self.text_box_empty=pg.transform.scale(self.text_box_empty, (self.width,self.height*0.35))
        self.screen.blit(self.text_box_empty,(0,self.height*0.65))
    
    def draw_action_box(self):
        self.action_box=pg.transform.scale(self.action_box,(self.width*0.22, self.height*0.4))
        self.screen.blit(self.action_box,(self.width*0.687,self.height*0.62))

    def draw_pkmn_info_box_enemy(self):
        self.screen.blit(self.pkmn_info_box_enemy,(self.width*0.05,0))
    
    def draw_pkmn_info_box_player(self):
        self.screen.blit(self.pkmn_info_box_player,(self.width*0.52,self.height*0.4222))