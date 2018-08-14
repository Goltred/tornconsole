"""
Bazaar information related classes
"""

import curses
import constants
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
                #Evaluate the conditions based on the settings
                #Will add if the setting is set to False or it is true and 
                #is on the market_watched_items list
                only_watched = self.main.settings.bazaar_watched_items
                item_check = json_item['name'] in self.main.settings.watched_items
                add_item = True if (only_watched and item_check) or not only_watched else False

                if add_item:
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
            msg = "Your bazaar is not accessible right now"

            #Change the message based on the availability of the bazaar and 
            #the bazaar_watched_items settings
            if self.main.user_response["bazaar"] is not None and only_watched:
                msg = "None of your watched items are in your Bazaar"

            self.new_line(msg, contents)
        else:
            for item in sorted(self.items, key=lambda x: x.name):
                printed = False
                if self.main.windows["market"] is not None:
                    #Check if the item is on the market's items attribute
                    market_item = [mi for mi in self.main.windows["market"].items if mi.name == item.name]
                    if market_item:
                        if item.price <= market_item[0].cost:
                            #The item in the bazaar is the lowest priced or at least the same price
                            self.new_line(item.__str__(), contents, attributes=curses.color_pair(constants.COLOR_GREEN.index))
                            printed = True
                        elif item.price > market_item[0].cost:
                            #Item is more expensive
                            self.new_line(item.__str__(), contents, attributes=curses.color_pair(constants.COLOR_RED.index))
                            printed = True
                
                if not printed:
                    self.new_line(item.__str__(), contents)