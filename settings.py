"""
Class that holds the values inside the settings.ini file
"""
import curses
import os
from window import Window
from shutil import copyfile

class TornSettings():
    key = None
    refresh_interval = None
    watched_items = None

    def __init__(self, *args, **kwargs):
        for k, v in kwargs.items():
            if hasattr(self, k):
                if k == "watched_items":
                    items = [int(i.strip()) for i in v.split(",")]
                    v = items

                setattr(self, k, v)

        #Validate that basic settings are present
        errors = []
        base_msg = "{} could not be found in the settings file"
        if self.key is None:
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
            