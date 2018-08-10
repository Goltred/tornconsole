class TornItem(object):
    """
    Definition of an Item in torn based on its values in the JSON
    response of an API call performed against the Torn endpoint
    """

    name = ""
    description = ""
    type = ""
    buy_price = -1
    sell_price = -1
    market_value = -1
    circulation = -1
    image = ""
    id = -1

    def __init__(self, id, *args, **kwargs):
        self.id = int(id)

        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)

class TornInfo(object):
    """
    Class holding methods and dictionaries related to the API call
    performed against the Torn endpoint
    """

    items = None

    def __init__(self, *args, **kwargs):
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)

    def get_item_by_name(self, name):
        """
        Look on the items attribute and return the items that match
        the given name
        """

        for item_id, item_details in self.items.items():
            if name.lower().strip() == item_details["name"].lower().strip():
                item = TornItem(item_id, **item_details)
                return item
