from status import StatusWindow
from travel import TravelWindow
from bazaar import BazaarWindow
from market import MarketWindow
from update_status import UpdateStatusWindow
from attacks import AttackWindow
from notifications import NotificationsWindow
from chain import ChainWindow
"""
Constants for the application
"""

HOME_URL = "www.torn.com"
LINES = 70
COLUMNS = 170

WINDOWS = {}

WINDOWS["status"] = {"type": StatusWindow, "h": 11, "w": 50, "y": 0, "x": 0}
WINDOWS["travel"] = {"type": TravelWindow, "h": 11, "w": 46, "y": 0, "x": WINDOWS["status"]["w"]}
WINDOWS["chain"] = {"type": ChainWindow, "h": 8, "w": 66, "y": 0, "x": WINDOWS["travel"]["x"] + WINDOWS["travel"]["w"]}

WINDOWS["bazaar"] = {"type": BazaarWindow, "h": 20, "w": 50, "y": WINDOWS["status"]["h"], "x": 0}
WINDOWS["market"] = {"type": MarketWindow, "h": 20, "w": 46, "y": WINDOWS["status"]["h"], "x": WINDOWS["bazaar"]["x"] + WINDOWS["bazaar"]["w"]}
WINDOWS["attacks"] = {"type": AttackWindow, "h": LINES - WINDOWS["chain"]["h"] - 1, "w": WINDOWS["chain"]["w"], "y": WINDOWS["chain"]["h"], "x": WINDOWS["chain"]["x"]}
WINDOWS["notifications"] = {"type": NotificationsWindow, "h": 14, "w": WINDOWS["status"]["w"] + WINDOWS["travel"]["w"], "y": WINDOWS["bazaar"]["y"] + WINDOWS["bazaar"]["h"], "x": 0}
WINDOWS["update"] = {"type": UpdateStatusWindow, "h": 1, "w": COLUMNS, "y": LINES - 1, "x": 0}

CONSOLE_WINDOW_HEIGHT = 5

#Endpoints
USER_ENDPOINT = "https://api.torn.com/user"
TORN_ENDPOINT = "https://api.torn.com/torn"