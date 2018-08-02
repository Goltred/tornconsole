"""
Classes related to the Status of the character. Including
character bars
"""

import curses
import time
import utility
from window import Window
from statusbar import StatusBar

class ChainWindow(Window):
    """
    curses window displaying chain information
    """

    chain = None

    def __init__(self, *args, **kwargs):
        super(ChainWindow, self).__init__(*args, **kwargs)
        self.timestamp = None

    def get_counter(self, seconds):
        """
        Calculates and creates the timer string for the timers of the chain
        """

        self.timestamp = time.time() + seconds if self.timestamp is None else self.timestamp
        to_go_seconds = self.timestamp - time.time() if seconds > 0 else 0
        hours, minutes, seconds = utility.hms_from_seconds(to_go_seconds)
        counter_str = utility.format_hms(hours, minutes, seconds)

        #Hacky hacky fix. Remove the hour part from the timeout
        return counter_str[4:]

    def populate(self):
        for key, value in self.main.user_response.items():
            if hasattr(self, key):
                if key in ['chain']:
                    status_bar = StatusBar(key, **value)
                    value = status_bar

                setattr(self, key, value)

        self.window.border()

        #Create a new window for the character bars
        contents = self.window.derwin(1, 1)

        self.new_line("Chain Status",
                      contents,
                      attributes=curses.A_UNDERLINE | curses.A_BOLD
                      )
        self.new_line("", contents)
        if self.chain.cooldown > 0:
            #Chain is in cooldown. This has not been tested
            self.new_line(
                "{:8}: {}".format("Maximum", self.chain.maximum),
                contents
                )
            self.new_line(
                "{:8}: {}".format("Current", self.get_counter(self.chain.current)),
                contents
                )
            self.new_line(
                "{:8}: {}s".format("Cooldown", self.chain.cooldown),
                contents
                )
        else:
            #Chain in progress
            self.new_line(
                "{:8}: {}".format("Current", self.chain.current),
                contents
                )
            self.new_line(
                "{:8}: {}".format("Timeout", self.get_counter(self.chain.timeout)),
                contents
                )
            self.new_line(
                "{:8}: {}".format("Modifier", self.chain.modifier),
                contents
                )
