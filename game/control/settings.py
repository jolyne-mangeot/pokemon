import json
import os

from game._all_paths_ import CONTROL_SETTINGS_PATH, LANGUAGE_DIALOG_PATH, SAVES_PATH

class Settings:
    """
        Handles all parameters from imported settings.json file
    """

    def load_player_data(self) -> dict:
        """
            Loads all player save data from the saves directory
        """
        player_saves = []
        for player_save in os.listdir(SAVES_PATH):
            with open(SAVES_PATH + player_save, "r") as file:
                player_saves.append(json.load(file))
        return player_saves

    def load_language(self, language : str) -> dict:
        """
            Load the default English dialogues
        """
        with open(LANGUAGE_DIALOG_PATH + "en-en.json", "r") as file:
            default_dialogs = json.load(file)
        with open(LANGUAGE_DIALOG_PATH + language + ".json", "r") as file:
            dialogs = json.load(file)
        default_dialogs.update(dialogs)
        return default_dialogs
    
    def save_player_data(self, player_data : dict, save : str):
        """
            Saves player data into a JSON file
        """

        with open(SAVES_PATH + "save_" + save + "_pokedex.json", "w") as file:
            json.dump(player_data, file, indent=4)
    
    def reset_player_data(self, save : str):
        """
            Resets player save data by overwriting the file with an empty dictionary
        """
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