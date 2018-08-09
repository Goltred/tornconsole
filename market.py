"""
Bazaar information related classes
"""

import curses
from window import Window

class MarketBase(object):
    def __init__(self, *args, **kwargs):
        for k, v in kwargs.items():
            if hasattr(self, k):
                setattr(self, k, v)

class MarketItem(MarketBase):
    pass

class MarketPoint(MarketBase):
    cost = -1
    quantity = -1
    total_cost = -1

class Market(object):
    pointsmarket = None
    bazaar = None
    itemmarket = None

class MarketWindow(Window):
    items = []
    next_update = None

    def populate(self):
        #Draw the border and create the inside window
        self.window.border()
        contents = self.window.derwin(1, 1)

        #Add the default lines
        self.new_line("Watched Market Items", contents, attributes=curses.A_BOLD | curses.A_UNDERLINE)
        self.new_line("", contents)

        if self.main.settings.watched_items:
            items = self.main.settings.watched_items

            for i in items:
                if i != "point":
                    #Get the item information from the torninfo object
                    item = self.main.torninfo.get_item_by_name(i)
                    if item:
                        pass
                        #Query the Torn API with the item id
                        #self.main.tornapi.get_market(item.id)
                else:
                    #Get the first item from the pointsmarket key
                    selections=["pointsmarket"]
                    #self.pointsmarket = self.main.tornapi.get_market(selections = selections)
                
                #Get the cheapest between bazaars and market

                item_line = "{} ({})".format(item.name, item.id)

                
                self.new_line(item_line, contents)
        else:
            self.new_line("No items configured in settings.ini", contents)
