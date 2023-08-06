"""
Copyright (c) 2023 Collin Meyer

REST API client for interacting with Atlassian Confluence

Description of how these API's work can be found here:
https://developer.atlassian.com/server/confluence/confluence-json-rpc-apis/

API Methods can be found here:
https://developer.atlassian.com/server/confluence/remote-confluence-methods/

API Data Objects can be found here:
https://developer.atlassian.com/server/confluence/remote-confluence-data-objects/
"""

import requests

from confclient.confexcept import BadRestRequestException


# ---------------------- CONSTANTS ----------------------

REST_ENDPOINT = "/rest/api"

# ----------------- Class Definitions -------------------


class RestClient:
    """Rest client for interacting with confluence

    Attributes:
        url: Base Url of Confluence server, e.g. https://my.confluence.server.com
        username: str = Username of Confluence user with administrator privelege
        password: str = Password of Confluence user with administrator privelege
                NOTE: Many functionalities will fail without administrator privelege!
    """

    def __init__(self, url, username, password):
        self.url = url
        self.username = username
        self.password = password

    def _execute_rest(
        self, api_path: str, data: dict = None, params: dict = None
    ) -> requests.Response:
        response = requests.get(
            self.url + REST_ENDPOINT + api_path,
            json=data,
            params=params,
            auth=requests.auth.HTTPBasicAuth(self.username, self.password),
            timeout=10,
        )

        if response.status_code != 200:
            raise BadRestRequestException(
                f"Error: Status Code {response.status_code} Encountered,\n{response.text}"
            )

        return response

    def get_users_in_group(self, groupname: str, **params) -> dict:
        """Perform rest API call to get users in a specific group

        Args:
            groupname: str = Name of group to get users from

        Returns:
            List of Dictionaries containing user information
        """
        res = self._execute_rest(f"/group/{groupname}/member", params=params).json()

        return {
            "users": [
                {
                    "username": i["username"],
                    "userKey": i["userKey"],
                    "displayname": i["displayName"],
                }
                for i in res["results"]
            ]
        }

    def get_groups(self, **params) -> dict:
        """Perform rest API call to get users in a specific group

        Returns:
            List of Dictionaries containing group information as
            well as start and limit from server
        """
        res = self._execute_rest("/group", params=params).json()

        return {
            "groups": [
                {
                    "groupname": i["name"],
                    "link": i["_links"]["self"],
                }
                for i in res["results"]
            ],
            "start": res["start"],
            "limit": res["limit"],
        }

    def get_all_users(self, limit: int, start: int) -> dict:
        """Perform rest API call to get users in a specific group

        Args:
            limit: Max number of users to return
            start: Beginning index to search for users

        Returns:
            List of Dictionaries containing user information
        """
        return self.get_users_in_group("confluence-users", limit=limit, start=start)
