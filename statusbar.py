import utility

class StatusBar:
    current = None
    maximum = None
    increment = None
    interval = None
    ticktime = None
    fulltime = None
    timeout = None
    modifier = None
    cooldown = None

    def __init__(self, name, *args, **kwargs):
        self.name = name
        for k, v in kwargs.items():
            if hasattr(self, k):
                setattr(self, k, v)

    def __str__(self):
        hours, minutes, seconds = utility.hms_from_seconds(self.fulltime)
        if (hours, minutes, seconds) == (0,0,0):
            full_str = "(Full)"
        else:
            full_str = "(Full in: {})".format(utility.format_hms(hours, minutes, seconds))
        
        return "{:6}: {:<5}/{:<5} {}".format(self.name, self.current, self.maximum, full_str)
