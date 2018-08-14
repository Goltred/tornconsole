"""
Bazaar information related classes
"""

import curses
import time
import threading
from window import Window
from torninfo import TornItem

class MarketBase(object):
    def __init__(self, *args, **kwargs):
        for k, v in kwargs.items():
            if hasattr(self, k):
                setattr(self, k, v)

class MarketItem(MarketBase):
    id = -1
    name = None
    cost = None
    quantity = None
    market = ""

class MarketPoint(MarketItem):
    total_cost = -1

class Market(MarketBase):
    name = None
    pointsmarket = None
    bazaar = None
    itemmarket = None

class MarketWindow(Window):
    items = []
    market_update = None
    market_thread = None

    def validate_duplicate_items(self, name):
        for item in self.items:
            if name.lower() == item.name.lower():
                #The item is alraedy there
                return False

        return True

    def get_cheapest(self, name, id, market_name, market):
        cheapest = sorted(market.items(), key=lambda x: x[1]["cost"])[0]

        #Add the missing values to the API response
        cheapest[1]["name"] = name
        cheapest[1]["id"] = id
        cheapest[1]["market"] = market_name

        return cheapest[1]

    def update_market_items(self):
        #Update the information for each item
        for name in self.main.settings.watched_items:
            id = ""

            if self.validate_duplicate_items(name):
                if name.lower() != "point":
                    selections = ["bazaar", "itemmarket"]
                    #Get the item information first
                    item = self.main.torninfo.get_item_by_name(name)
                    id = item.id
                else:
                    selections = ["pointsmarket"]

                #Now get the information from the market
                market_response = self.main.tornapi.get_market(id, selections = selections)
                market_info = Market(**market_response)

                #Get the cheapest item
                market_item = None
                if name.lower() != "point":
                    #Check the bazaars and create an object
                    cheapest_bazaar = self.get_cheapest(name, item.id, "Bazaar", market_info.bazaar)
                    cheapest_bazaar_item = MarketItem(**cheapest_bazaar)

                    #Check the itemmarket and create an object
                    cheapest_market = self.get_cheapest(name, item.id, "Market", market_info.itemmarket)
                    cheapest_market_item = MarketItem(**cheapest_market)

                    market_item = cheapest_bazaar_item if cheapest_bazaar_item.cost <= cheapest_market_item.cost else cheapest_market_item
                else:
                    #Sort the results and get the cheapest
                    cheapest = self.get_cheapest("Point", -1, "Market", market_info.pointsmarket)
                    market_item = MarketPoint(**cheapest)

                if market_item:
                    self.items.append(market_item)

        self.window.refresh()

    def populate(self):
        #Draw the border and create the inside window
        self.window.border()
        contents = self.window.derwin(1, 1)

        #Add the default lines
        self.new_line("Watched Market Items", contents, attributes=curses.A_BOLD | curses.A_UNDERLINE)
        self.new_line("", contents)

        if self.main.settings.watched_items:
            #Set the next update
            if self.market_update is None or self.market_update <= time.time():
                self.items = []
                #Start the method to update the items in a new thread to allow the rest of the
                #windows to render
                if self.market_thread is None or not self.market_thread.is_alive():
                    t = threading.Thread(target=self.update_market_items, name="Thread-{}".format("UpdateMarket"), daemon=True)
                    self.market_thread = t
                    self.market_thread.start()

                #Set the next_update value so that it refreshes in the next minute
                self.market_update = time.time() + int(self.main.settings.market_refresh_interval)

            #Display the items
            for item in sorted(self.items, key=lambda x: x.name):
                item_line = "[{}] {:21}: ${:,.0f}".format(item.market, item.name, item.cost)

                self.new_line(item_line, contents)
        else:
            self.new_line("No items configured in settings.ini", contents)
