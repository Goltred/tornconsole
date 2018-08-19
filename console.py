"""
Console window where the user is able to input commands to change
the layout or options of the application
"""

import curses
from window import Window

class ConsoleWindow(Window):
    """
    curses window that acts as a terminal console
    """
    history = []

    def populate(self):
        self.window.border()
        contents = self.window.derwin(1, 1)
        self.title("Console", contents)
        for line in self.history[:3]:
            self.new_line(line, contents)

class CommandWindow(Window):
    """
    curses window that acts as a terminal console
    """
    prompt = ">"
    command = ""
    history = []

    def get_character(self):
        """
        Parse the keyboard key pressed by the user
        """
        character = self.window.getch()
        if character == curses.KEY_ENTER:
            #Do command
            pass
        else:
            self.command += character

    def populate(self):
        self.window.border()
        contents = self.window.derwin(1, 1)
        for line in self.history[:3]:
            self.new_line(line, contents)
        self.new_line(self.prompt, contents, False)
        self.get_character()