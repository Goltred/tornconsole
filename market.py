"""
Bazaar information related classes
"""

import curses
from window import Window

class MarketItem:
    def __init__(self, *args, **kwargs):
        for k, v in kwargs.items():
            if hasattr(self, k):
                setattr(self, k, v)

class MarketWindow(Window):
    items = []

    def populate(self):
        #Placeholder

        #Draw the border and create the inside window
        self.window.border()
        contents = self.window.derwin(1, 1)

        #Add the default lines
        self.new_line("Watched Market Items", contents, attributes=curses.A_BOLD | curses.A_UNDERLINE)
        self.new_line("", contents)
        self.new_line("Not implemented yet :(", contents)
