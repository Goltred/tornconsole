"""
Class that holds the values inside the settings.ini file
"""
import curses
import os
from window import Window
from shutil import copyfile

class TornSettings():
    api_key = None
    refresh_interval = None
    watched_items = None
    min_attack_respect = 3
    market_refresh_interval = 60
    bazaar_watched_items = False

    def __init__(self, *args, **kwargs):
        for key, value in kwargs.items():
            if hasattr(self, key):
                if key == "watched_items":
                    items = [i.strip() for i in value.split(",")]
                    value = items
                elif key == "min_attack_respect":
                    value = float(value)
                elif key == "bazaar_watched_items":
                    value = True if value.lower() in [1, "yes", "true"] else False

                setattr(self, key, value)

        #Validate that basic settings are present
        errors = []
        base_msg = "{} could not be found in the settings file"
        if self.api_key is None:
            errors.append(base_msg.format("API KEY"))

        if self.refresh_interval is None:
            errors.append(base_msg.format("REFRESH INTERVAL"))

        if errors:
            msg = "Errors found:\n" + "\n".join(errors)
            msg += "\n\nPlease validate your settings.ini file"
            raise Exception(msg)

class SettingsWindow(Window):
    def populate(self):
        debug = self.window.derwin(50, 1)
        self.new_line("No settings file found.")
        self.new_line("Creating new settings.ini")
        try:
            current_directory = os.path.abspath(".")
            example_path = os.path.abspath("settings.ini.example")
            settings_path = os.path.abspath("settings.ini")
            if os.path.exists(example_path):
                copyfile(example_path, settings_path)
            else:
                raise IOError("Could not find example settings file in {}".format(example_path))

            created = False
            with open(settings_path, "r") as f:
                created = True

            if created:
                self.new_line("Created new settings.ini")
                self.new_line("Please, open the file located at {} and fill the base information".format(settings_path))
        except IOError:
            self.new_line("ERROR: Could not create the settings.ini file")
            self.new_line("Please, go to {}, rename settings.ini.example to settings.ini and fill the base information".format(current_directory))

        self.wait_for_key_press()
            