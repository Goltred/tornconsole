"""
Classes and methods related to TornAPI calls
"""

import requests
import json
import constants

class TornAPI:
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

    def get_user(self, user_id=None, selections=[]):
        """
        Call the TornAPI User endpoint and retrieve the information
        for the specified user_id
        """

        id = "" if user_id is None else user_id
        sel = ",".join(selections)
        response = self.get("{}/{}?selections={}&key={}".format(constants.USER_ENDPOINT, user_id, sel, self.key))
        return response.json()

    def get_torn(self, id=None, selections=[]):
        sel = ",".join(selections)
        response = self.get("{}/{}?selections={}&key={}".format(constants.TORN_ENDPOINT, id, sel, self.key))
        return response.json()