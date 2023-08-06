"""
Copyright (c) 2023 Collin Meyer

JSON RPC client for interacting with Atlassian Confluence.
This protocol is only used because the REST API does not expose
many needed functionalities

Description of how these API's work can be found here:
https://developer.atlassian.com/server/confluence/confluence-json-rpc-apis/

API Methods can be found here:
https://developer.atlassian.com/server/confluence/remote-confluence-methods/

API Data Objects can be found here:
https://developer.atlassian.com/server/confluence/remote-confluence-data-objects/
"""

import random
import requests

from confclient.confexcept import BadRPCRequestException

# ---------------------- CONSTANTS ----------------------

RPC_ENDPOINT = "/rpc/json-rpc/confluenceservice-v2"

# ----------------- Class Definitions -------------------


class RPCClient:
    """RPCClient for interacting with Confluence

    Attributes:
        url: str = Base Url of Confluence server, e.g. https://my.confluence.server.com
        username: str = Username of Confluence user with administrator privelege
        password: str = Password of Confluence user with administrator privelege
                NOTE: Many functionalities will fail without administrator privelege!
    """

    def __init__(self, url: str, username: str, password: str, version="2.0"):
        """Stores attributes needed for API calls

        See argument explanations above
        """
        self.url = url
        self.username = username
        self.password = password
        self.version = version

    def _execute_rpc(
        self, method: str, params: list[str | dict | bool]
    ) -> requests.Response:
        """Preform API call to endpoint

        Args:
            method: str = The RPC method to be called
            params: list = The arguments you would like to

        Returns:
            HTTP Request Response -> intentionally returning all info,
                                     to be dealt with upstream
        """

        data = {
            "jsonrpc": self.version,
            "method": method,
            "params": params,
            "id": random.randint(1000, 2000),
        }

        response = requests.post(
            self.url + RPC_ENDPOINT,
            json=data,
            auth=requests.auth.HTTPBasicAuth(self.username, self.password),
            timeout=10,
        )

        # Ensure non-failed request, fail hard and fast
        # UPDATE: RPC always returns 200 status code
        # if response.status_code != 200:
        #     raise BadRPCRequestException(
        #         f"Error: Status Code {response.status_code} Encountered,\n{response.text}"
        #     )

        if "error" in response.json():
            error = response.json()["error"]
            raise BadRPCRequestException(f"Error ({error['code']}): {error['message']}")

        return response

    def add_user(
        self,
        username: str,
        fullname: str,
        email: str,
        password: str = "Credential.NONE",
        notify_user: bool = False,
    ) -> requests.Response:
        """Invoke RPC endpoint for creating a new user in Confluence

        RPC documentation here:
            https://developer.atlassian.com/server/confluence/remote-confluence-methods/#user-management
                - addUser

        NOTE: This method uses the addUser RPC method which includes the boolean notifyUser flag

        Args:
            username: str = Confluence username of user to create
            fullname: str = first + last name of user to create
            email: str = email of user to create
            password: str = password of user to create, when left default users
                            will have to 'reset password' before logging in
            notify_user: bool = flag to indicate whether or not to send users an email
                                notifying them of account creation

        Returns:
            RPC API request response
        """

        return self._execute_rpc(
            "addUser",
            [
                {"name": username, "fullname": fullname, "email": email},
                password,
                notify_user,
            ],
        )

    def remove_user(self, username: str) -> requests.Response:
        """Invoke RPC endpoint for creating a new user in Confluence

        RPC documentation here:
            https://developer.atlassian.com/server/confluence/remote-confluence-methods/#user-management
                - removeUser

        NOTE: This method uses the addUser RPC method which includes the boolean notifyUser flag

        Args:
            username: str = Confluence username of user to create

        Returns:
            RPC API request response
        """

        return self._execute_rpc("removeUser", [username])

    def add_user_to_group(self, username: str, group: str) -> requests.Response:
        """Invoke RPC endpoint for adding user to a group in Confluence

        RPC documentation here:
            https://developer.atlassian.com/server/confluence/remote-confluence-methods/#user-management
                - addUserToGroup

        Args:
            username: str = Confluence username of user to add to group
            group: str = name of the group to add the user to

        Returns:
            RPC API request response
        """

        return self._execute_rpc("addUserToGroup", [username, group])

    def remove_user_from_group(self, username: str, group: str) -> requests.Response:
        """Invoke RPC endpoint for removing a user form a group in Confluence

        RPC documentation here:
            https://developer.atlassian.com/server/confluence/remote-confluence-methods/#user-management
                - removeUserFromGroup

        Args:
            username: str = Confluence username of user to remove from the group
            group: str = name of the group to remove the user from

        Returns:
            RPC API request response
        """

        return self._execute_rpc("removeUserFromGroup", [username, group])

    def add_group(self, group):
        """Invoke RPC endpoint for creating a new group in Confluence

        RPC documentation here:
            https://developer.atlassian.com/server/confluence/remote-confluence-methods/#user-management
                - addGroup

        Args:
            group: str = name of the group to create

        Returns:
            RPC API request response
        """

        return self._execute_rpc("addGroup", [group])

    def remove_group(self, group):
        """Invoke RPC endpoint for removing group in Confluence

        RPC documentation here:
            https://developer.atlassian.com/server/confluence/remote-confluence-methods/#user-management
                - removeGroup

        Args:
            group: str = name of the group to remove

        Returns:
            RPC API request response
        """

        return self._execute_rpc("removeGroup", [group, ""])
