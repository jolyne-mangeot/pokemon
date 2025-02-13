import json
import os
import pygame as pg
from control.__control_settings__ import CONTROL_SETTINGS_PATH, LANGUAGE_DIALOG_PATH, SAVES_PATH

class Settings:
    def load_language(self, language : str) -> dict:
        with open(LANGUAGE_DIALOG_PATH + "en-en.json", "r") as file:
            default_dialogs = json.load(file)
        with open(LANGUAGE_DIALOG_PATH + language + ".json", "r") as file:
            dialogs = json.load(file)
        default_dialogs.update(dialogs)
        return default_dialogs

    def load_player_data(self) -> dict:
        player_saves = []
        for player_save in os.listdir(SAVES_PATH):
            with open(SAVES_PATH + player_save, "r") as file:
                player_saves.append(json.load(file))
        return player_saves
    
    def save_player_data(self, player_data : dict, save : str):
        with open(SAVES_PATH + "save_" + save + "_pokedex.json", "w") as file:
            json.dump(player_data, file, indent=4)
    
    def reset_player_data(self, save : str):
        with open(SAVES_PATH + "save_" + save + "_pokedex.json", "w") as file:
            json.dump({}, file, indent=4)     

    def load_settings(self):
        """
            load settings from json file with set path
        """
        with open(CONTROL_SETTINGS_PATH, "r") as file:
            settings = json.load(file)
        return settings
    
    def save_settings(self, settings):
        """
            save settings into json file with set path
        """
        with open(CONTROL_SETTINGS_PATH, "w") as file:
            json.dump(settings, file, indent=4)