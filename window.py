"""
Main Window class definition that is parent of other windows
within the app
"""

import curses
import time

class Window:
    h = None
    w = None
    y = None
    x = None

    def __init__(self, main, name, h, w, y, x):
        self.name = name
        self.window = curses.newwin(h, w, y, x)
        self.main = main

        #Store the attributes of the window
        self.h = h
        self.w = w
        self.y = y
        self.x = x

    def update(self, refresh_interval=5):
        """Redraw the window and its contents"""
        self.refresh_interval = refresh_interval
        self.next_update = time.time() + self.refresh_interval

        self._redraw()

    def _redraw(self):
        """
        Clear and perform the actual refresh of the window
        """

        self.window.clear()
        self.populate()
        self.window.refresh()

    def populate(self):
        """
        Main method intended to hold the information that should be
        inside the window
        """

        self.new_line("Not implemented")

    def wait_for_key_press(self):
        self.new_line("Press any key to continue", add_newline=False)
        self.window.getch()

    def get_command(self, debug_window = None):
        """
        Allows for the user to press keys, concatenating a string until the ENTER key is pressed
        """
        command = ""
        x = 0
        y = 0
        while True:
            c = self.window.getch()

            if c == ord("\n"):
                return command
            elif c in (curses.KEY_DC,):
                x -= 1
                self.delete()
                self.refresh()
            elif c == curses.KEY_LEFT:
                x -= 1
            elif c == curses.KEY_RIGHT:
                x += 1
            elif c == curses.KEY_HOME:
                x = y = 0
            else:
                command += chr(c)
                x += 1

            self.new_line(x, debug_window)

    def new_line(self, text, target_window=None, add_newline=True, attributes=0, pos=None):
        """
        Add a new string to the target_window. Attributes indicate what curses
        properties are to be added to the string
        """

        target_window = self.window if target_window == None else target_window
        
        #Check if the text is going to go over the size of the window
        max_y, max_x = target_window.getmaxyx()

        if len(text) > max_x:
            #Shorten the text to fit the contents of the window and add ...
            text = "{}...".format(text[:max_x - 4])

        try:
            if pos is None:
                target_window.addstr(text, attributes)
            else:
                target_window.addstr(pos[0], pos[1], text, attributes)

            if add_newline:
                    target_window.addstr("\n")
        except Exception as e:
            #Chances are that this is trying to add a new line and going
            #outside of the window geometry
            if e.args[0] == 'addwstr() returned ERR':
                pass