"""
Classes and methods related to TornAPI calls
"""

import requests
import json
import constants

class TornAPI:
    user_calls = 0
    market_calls = 0
    torn_calls = 0
    def __init__(self, key):
        self.key = key

    def get(self, url):
        """
        Perform and handle TornAPI calls
        """

        response = requests.get(url)
        assert response.status_code == 200
        response_json = response.json()

        if "error" not in response_json.keys():
            return response
        else:
            #An error occurred
            code = response_json["error"]["code"]
            error = response_json["error"]["error"]
            raise Exception("An error has occurred while querying the Torn API\nCode: {}\nError: {}".format(code, error))

    def _make_call(self, endpoint, id, selections):
        sel = ",".join(selections)
        response = self.get("{}/{}?selections={}&key={}".format(endpoint, id, sel, self.key))
        
        return response.json()

    def get_user(self, user_id=None, selections=[]):
        """
        Call the TornAPI User endpoint and retrieve the information
        for the specified user_id
        """

        id = "" if user_id is None else user_id
        self.user_calls += 1
        return self._make_call(constants.USER_ENDPOINT, id, selections)

    def get_torn(self, id=None, selections=[]):
        """
        Call the TornAPI Torn endpoint
        """
        self.torn_calls += 1
        return self._make_call(constants.TORN_ENDPOINT, id, selections)

    def get_market(self, id=None, selections=[]):
        self.market_calls += 1
        return self._make_call(constants.MARKET_ENDPOINT, id, selections)