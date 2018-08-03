import datetime
from html.parser import HTMLParser

DEFAULT_TIME_FORMAT = '%Y-%m-%d %H:%M:%S'
DEFAULT_HMS_FORMAT = "{:02}h {:02}m {:02}s"

def hms_from_seconds(seconds):
    """
    Return the hours, minutes and seconds from the total number of
    seconds
    """

    delta = datetime.timedelta(seconds=seconds)
    hours, remainder = divmod(delta.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)

    return hours, minutes, seconds

def format_hms(hours, minutes, seconds, format=DEFAULT_HMS_FORMAT):
    return format.format(hours, minutes, seconds)

def format_timestamp(timestamp, format=DEFAULT_TIME_FORMAT):
    """
    Return a formatted string according to the format
    parameter based from a given timestamp
    """
    return datetime.datetime.fromtimestamp(timestamp).strftime(format)


class HTMLStripper(HTMLParser):
    def __init__(self):
        super(HTMLStripper, self).__init__()
        self.html_data = ""

    def handle_data(self, data):
        self.html_data += data

    def get_data(self):
        return self.html_data.replace("[view]", "").strip()

def strip_tags(html):
    parser = HTMLStripper()
    parser.feed(html)
    return parser.get_data()
