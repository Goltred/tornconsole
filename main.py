import curses
import requests
import time
import threading
import signal

from constants import *
from window import Window
from console import ConsoleWindow
from settings import TornSettings, SettingsWindow
from tornapi import TornAPI
from torninfo import TornInfo

class Main:
    """Main window class. Contains the main logic for the console application"""
    windows = {}
    settings = None
    refresh_threads = {}
    
    def create_window(self, name, type, h, w, y, x):
        """
        Create a window with the given attributes and type
        """

        #Check if the name already exists
        check = name in self.windows.keys()

        if not check:
            window = type(self, name, h, w, y, x)
            self.windows[name] = window
            return window
        else:
            raise Exception("Window already exists")

    def _start_refresh_thread(self, window):
        """Create a new thread and start the window.update method in it"""

        t = threading.Thread(target=window.update, name="Thread-{}".format(window.name), daemon=True)
        self.refresh_threads[window.name] = t
        self.refresh_threads[window.name].start()

    def _refresh_window(self, window):
        """
        Private method that validates if a new thread is needed for a give window
        or if one already existed that needs to be recreated
        """

        if window.name not in self.refresh_threads.keys():
            #Create a new thread for the window
            self._start_refresh_thread(window)
        else:
            #Check if the thread is still alive and recreate the thread if it is not
            t = self.refresh_threads[window.name]
            if not t.is_alive():
                self._start_refresh_thread(window)

    def start_refresh_window(self, name = None, in_thread=False, exclude=[]):
        """
        Start the update for all windows, named or all except for the
        ones added to the exclude parameter
        """

        if name is None:
            for _, window in self.windows.items():
                if window.name not in exclude:
                    if not in_thread:
                        window.update()
                    else:
                        _refresh_window(window)
        else:
            window = self.windows[name]

            if not in_thread:
                window.update()
            else:
                _refresh_window(window)

    def create_windows(self):
        """
        Create the windows of the application
        """

        #Create the windows defined in the constants
        for w, d in WINDOWS.items():
            self.create_window(w, **d)

        ##Create the status window
        #self.create_window("status", StatusWindow, *STATUS_WINDOW_DEF)

        ##Create the travel window
        #self.create_window("travel", TravelWindow, *TRAVEL_WINDOW_DEF)

        ##Create the update status window
        #self.create_window("update_status", UpdateStatusWindow, *UPDATE_STATUS_WINDOW_DEF)

        #Create the actual console window where commands are output
        #self.console = self.create_window("console", ConsoleWindow, CONSOLE_WINDOW_HEIGHT, curses.COLS, curses.LINES - CONSOLE_WINDOW_HEIGHT - 1, 0)

    def change_location(self, callback):
        """
        Future feature. Display different windows/options based on in-game
        location. e.g. Torn, China, etc.
        """
        raise NotImplementedError

    def create_settings(self):
        """Prompt the user for required settings for the application to run"""
        settings_window = SettingsWindow(self, "settings", curses.LINES, curses.COLS, 0, 0)
        settings_window.populate()

    def check_settings(self):
        """
        Read the settings.ini file and create the TornSettings object.
        If no settings.ini file exists, prompt for the values in it and
        create one
        """

        lines = []
        processed = False
        try:
            with open("settings.ini", "r") as f:
                lines = f.readlines()

            settings_dict = {}
            for l in lines:
                if l.strip() != "" and l[0] != "#":
                    key = l.split("=")[0].strip()
                    value = l.split("=")[1].strip()

                    if "API_KEY" in key.upper():
                        settings_dict["key"] = value
                    elif "REFRESH_INTERVAL" in key.upper():
                        settings_dict["refresh_interval"] = value
                    elif "WATCHED_ITEMS" in key.upper():
                        settings_dict["watched_items"] = value

            processed = True
        except IOError:
            self.create_settings()

        if processed:
            settings = TornSettings(**settings_dict)
            return settings
        else:
            return False

    def run(self, stdscr):
        """Execute the terminal application"""
        stdscr.clear()
        curses.resize_term(LINES, COLUMNS)
        curses.curs_set(0)

        #Set the color pairs used by the application
        for color in COLOR_DEFS:
            curses.init_pair(*color)

        self.settings = self.check_settings()

        if self.settings is not None:
            #Create the tornapi object
            self.tornapi = TornAPI(self.settings.key)

            #Create the windows
            self.create_windows()

            #Setup selection variables
            user_selections=['basic', 'bars', 'travel', 'bazaar', 'attacks', 'events', 'messages']
            torn_selections=['items']

            #Refresh windows
            #Update the user response
            self.user_response = self.tornapi.get_user(selections=user_selections)
            self.torninfo = TornInfo(**self.tornapi.get_torn(selections=torn_selections))
            self.next_update = time.time() + int(self.settings.refresh_interval)
            while True:
                if time.time() >= self.next_update:
                    self.user_response = self.tornapi.get_user(selections=user_selections)
                    self.next_update = time.time() + int(self.settings.refresh_interval)

                #Call the update method of every window
                self.start_refresh_window()

            #Wait for user input
            #self.console.getstr(50, 1)
        else:
            #Settings are not present and could not be created
            pass

main = Main()

curses.LINES = LINES
curses.COLS = COLUMNS
curses.wrapper(main.run)