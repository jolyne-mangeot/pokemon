import json
from assets.__control_settings__ import CONTROL_SETTINGS_PATH

class Settings:
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