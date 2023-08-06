import requests

from confclient.confexcept import BadRestRequestException


class RestClient:
    def __init__(self, url, username, password):
        self.url = url
        self.username = username
        self.password = password

    def _execute(
        self, api_path: str, data: dict = None, params: dict = None
    ) -> requests.Response:
        response = requests.get(
            self.url + api_path,
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

    def getUsersInGroup(self, groupname: str, **params) -> dict:
        res = self._execute(f"/group/{groupname}/member", params=params).json()

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

    def getGroups(self, **params) -> dict:
        res = self._execute("/group", params=params).json()

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

    def getAllUsers(self, limit: int, start: int) -> dict:
        return self.getUsersInGroup("confluence-users", limit=limit, start=start)
