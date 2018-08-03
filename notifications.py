"""
Bazaar information related classes
"""

import datetime
import time
import curses
import utility
from window import Window
from collections import OrderedDict

class Notification:
    timestamp = None
    event = None
    seen = None
    sender_id = None
    name = None
    title = None
    read = None

    def __init__(self, *args, **kwargs):
        for k, v in kwargs.items():
            #Change the ID key since it is an actual function of a class
            if k == "ID":
                k = "sender_id"

            if hasattr(self, k):
                if k == "seen" or k == "read":
                    v = True if v == 1 else False

                setattr(self, k, v)

    def __str__(self):
        event_time = utility.format_timestamp(self.timestamp)
        if self.sender_id is None:
            #This is an event
            stripped_event = utility.strip_tags(self.event)
            msg = "{} - {}".format(event_time, stripped_event)
        else:
            #This is a message
            msg = "{} - {} ({}) says: {}".format(event_time, self.name, self.sender_id, self.title)

        return msg

class NotificationsWindow(Window):
    def populate(self):
        self.unseen = []
        max_items = 10
        
        #Join the messages and events
        notifications = {**self.main.user_response['events'], **self.main.user_response['messages']}

        #Sort them based on their timestamp
        notifications = OrderedDict(sorted(notifications.items(), key = lambda x: -x[1]["timestamp"]))

        for id in notifications:
            e = notifications[id]
            notification = Notification(**e)
            if not notification.seen:
                self.unseen.append(notification)

            if len(self.unseen) == max_items:
                break

        #Draw the border and create the inside window
        self.window.border()
        contents = self.window.derwin(1, 1)

        #Add the default lines
        self.new_line("Unseen Events or Messages", contents, attributes=curses.A_BOLD | curses.A_UNDERLINE)
        self.new_line("", contents)
        
        if len(self.unseen) == 0:
            self.unseen = []
            self.new_line("Nothing to see here... Move along.", contents, False, pos=(int(self.h/2), 0))
        else:
            for notification in self.unseen:
                self.new_line(notification.__str__(), contents)
