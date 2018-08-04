"""
Bazaar information related classes
"""

import curses
from window import Window

class BazaarItem:
    """
    Definition of a bazaar item based on the Torn API JSON response
    """
    id = None
    name = None
    type = None
    quantity = None
    price = None
    market_price = None

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)

    def __str__(self):
        return "{} x {}: ${}(RRP: ${})".format(
            self.quantity,
            self.name,
            self.price,
            self.market_price
            )

class BazaarWindow(Window):
    """
    curses window definition displaying the list of items in the player's
    bazaar along with their prize
    """
    items = []

    def populate(self):
        max_items = 10
        self.items = []
        if self.main.user_response['bazaar'] is not None:
            for json_item in self.main.user_response['bazaar']:
                #if json_item['ID'] in self.main.settings.watched_items:
                item = BazaarItem(**json_item)
                self.items.append(item)

                if len(self.items) == max_items:
                    break

        #Draw the border and create the inside window
        self.window.border()
        contents = self.window.derwin(1, 1)

        #Add the default lines
        self.new_line("My Bazaar", contents, attributes=curses.A_BOLD | curses.A_UNDERLINE)
        self.new_line("", contents)

        if not self.items:
            self.new_line("Bazaar is not accessible right now", contents)
        else:
            for item in self.items:
                self.new_line(item.__str__(), contents)
