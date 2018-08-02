"""
Console window where the user is able to input commands to change
the layout or options of the application
"""

import curses
from window import Window


class ConsoleWindow(Window):
    prompt = ">"
    command = ""
    history = []

    def get_character(self):
        ch = self.contents.getch()
        if ch == curses.KEY_ENTER:
            #Do command
            pass
        else:
            command += ch

    def populate(self):
        self.window.border()
        self.contents = self.window.derwin(1, 1)
        for line in history[:3]:
            self.new_line(line, contents)
        self.new_line(self.prompt, contents, False)
        self.get_character()