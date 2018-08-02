"""
Travel information window class
"""

import time
import curses
import utility
from window import Window

class TravelWindow(Window):
    destination = ""
    timestamp = 0
    departed = 0
    time_left = 0

    def populate(self):
        for k,v in self.main.user_response['travel'].items():
            if hasattr(self, k):
                setattr(self, k, v)

        #Draw the border and create the inside window
        self.window.border()
        contents = self.window.derwin(1, 1)

        #Add the default lines
        self.new_line("Travel Information", contents, attributes=curses.A_BOLD | curses.A_UNDERLINE)
        #self.new_line(" (Next Update in {})".format(next_update), contents)

        if self.time_left == 0:
            self.new_line("Not travelling", contents)
        else:
            #Travelling!
            #Set the seconds that we need to establish until the next update
            to_go_seconds = self.timestamp - time.time() if self.time_left > 0 else self.next_update - time.time()

            #Create the string
            hours, minutes, seconds = utility.hms_from_seconds(to_go_seconds)
            to_go = utility.format_hms(hours, minutes, seconds)

            departed_at = utility.format_timestamp(self.departed)
            arriving_at = utility.format_timestamp(self.timestamp)
            self.new_line("", contents)
            self.new_line("Travelling to {}".format(self.destination), contents)
            self.new_line("Flight departed at {}".format(departed_at), contents)
            self.new_line("Flight arriving at {}".format(arriving_at), contents)
            self.new_line("{} to go".format(to_go), contents)
