"""
Constants for the application
"""

import curses
from status import StatusWindow
from travel import TravelWindow
from bazaar import BazaarWindow
from market import MarketWindow
from update_status import UpdateStatusWindow
from attacks import AttackWindow
from notifications import NotificationsWindow
from chain import ChainWindow
from console import ConsoleWindow, CommandWindow

class ColorPair(object):
    index = None
    foreground = None
    background = None

    def __init__(self, index, foreground, background):
        self.index = index
        self.foreground = foreground
        self.background = background

    def __iter__(self):
        return iter([self.index, self.foreground, self.background])

HOME_URL = "www.torn.com"

#Window Size
LINES = 70
COLUMNS = 170

#curses windows definition
WINDOWS = {}

WINDOWS["status"] = {
    "type": StatusWindow,
    "h": 11, "w": 50,
    "y": 0, "x": 0
    }

WINDOWS["travel"] = {
    "type": TravelWindow,
    "h": 11, "w": 46,
    "y": 0, "x": WINDOWS["status"]["w"] #To the left of the status window
    }

WINDOWS["chain"] = {
    "type": ChainWindow,
    "h": 8, "w": 66,
    "y": 0, "x": WINDOWS["travel"]["x"] + WINDOWS["travel"]["w"]
    }

WINDOWS["bazaar"] = {
    "type": BazaarWindow,
    "h": 20, "w": 50,
    "y": WINDOWS["status"]["h"], "x": 0
    }

WINDOWS["market"] = {
    "type": MarketWindow,
    "h": 20, "w": 46,
    "y": WINDOWS["status"]["h"], "x": WINDOWS["bazaar"]["x"] + WINDOWS["bazaar"]["w"]
    }

WINDOWS["attacks"] = {
    "type": AttackWindow,
    "h": LINES - WINDOWS["chain"]["h"] - 1, "w": WINDOWS["chain"]["w"],
    "y": WINDOWS["chain"]["h"], "x": WINDOWS["chain"]["x"]
    }

WINDOWS["notifications"] = {
    "type": NotificationsWindow,
    "h": 14, "w": WINDOWS["status"]["w"] + WINDOWS["travel"]["w"],
    "y": WINDOWS["bazaar"]["y"] + WINDOWS["bazaar"]["h"], "x": 0
    }

WINDOWS["update"] = {
    "type": UpdateStatusWindow,
    "h": 1, "w": COLUMNS,
    "y": LINES - 1, "x": 0
    }

#Color definitions
COLOR_GREEN = ColorPair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
COLOR_RED = ColorPair(2, curses.COLOR_RED, curses.COLOR_BLACK)

#Color definitions are processed based on the following list
COLOR_DEFS = [COLOR_GREEN, COLOR_RED]

#Console height, this will probably be deprecated
after_notifications = WINDOWS["notifications"]["y"] + WINDOWS["notifications"]["h"]
CONSOLE_WINDOW = {
    "type": ConsoleWindow,
    "h":LINES - after_notifications - 4, "w": WINDOWS["attacks"]["x"],
    "y":after_notifications, "x":0
    }

COMMAND_WINDOW = {
    "type": CommandWindow,
    "h": 3, "w": CONSOLE_WINDOW["w"],
    "y": CONSOLE_WINDOW["y"] + CONSOLE_WINDOW["h"], "x": 0
    }

#Endpoints
USER_ENDPOINT = "https://api.torn.com/user"
TORN_ENDPOINT = "https://api.torn.com/torn"
MARKET_ENDPOINT = "https://api.torn.com/market"
