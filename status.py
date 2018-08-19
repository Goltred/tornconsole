"""
Classes related to the Status of the character. Including
character bars
"""

import curses
import utility
import constants
from window import Window
from statusbar import StatusBar

class StatusWindow(Window):
    name = ""
    player_id = ""
    status = ""
    happy = None
    life = None
    energy = None
    nerve = None

    def populate(self):
        for k,v in self.main.user_response.items():
            if hasattr(self, k):
                if k in ['happy', 'life', 'energy', 'nerve', 'chain']:
                    bar = StatusBar(k, **v)
                    v = bar

                setattr(self, k, v)

        self.window.border()
        
        #Create a new window for the character bars
        contents = self.window.derwin(1,1)

        self.title("Status Window", contents)
        self.new_line("", contents)
        self.new_line("{:6}: {}[{}]".format("Name", self.name, self.player_id), contents)
        self.new_line("{:6}: {}".format("Status", self.status[0]), contents)

        #Life
        self.new_line(self.life.__str__(), contents, attributes=curses.color_pair(constants.COLOR_GREEN.index))

        #Energy
        self.new_line(self.energy.__str__(), contents)

        #Nerve
        self.new_line(self.nerve.__str__(), contents)

        #Happiness
        self.new_line(self.happy.__str__(), contents)