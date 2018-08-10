"""
Status Bar where information about the app or next updates are given
"""

from window import Window
import time
import curses

class UpdateStatusWindow(Window):
    def __init__(self, *args, **kwargs):
        #Override the default init so that the whole window appears with a different background
        super(UpdateStatusWindow, self).__init__(*args, **kwargs)
        self.window.bkgd(" ", curses.A_REVERSE)

    def populate(self):
        for k,v in self.main.user_response.items():
            if hasattr(self, k):
                if k in ['happy', 'life', 'energy', 'nerve']:
                    bar = StatusBar(k, **v)
                    v = bar

                setattr(self, k, v)

        next_update = self.main.next_update - time.time()
        user_calls = self.main.tornapi.user_calls
        torn_calls = self.main.tornapi.torn_calls
        market_calls = self.main.tornapi.market_calls
        total = user_calls + torn_calls + market_calls

        update_str = "Next Update in {:.0f}s".format(next_update)
        calls_str = "Total Calls = {} ({} User, {} Market, {} Torn)".format(total, user_calls, market_calls, torn_calls)
        
        self.new_line("{} | {}".format(update_str, calls_str), add_newline = False)