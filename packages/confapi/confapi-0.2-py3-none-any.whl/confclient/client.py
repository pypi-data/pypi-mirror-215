"""



"""

from confclient.restclient import RestClient
from confclient.rpcclient import RPCClient


class ConfClient(RestClient, RPCClient):
    """Confluence API Client

    This class consists of all the different API clients that make
    the 1 unified confluence client
    """

    def __init__(self, url, username, password):
        RestClient.__init__(self, url, username, password)
        RPCClient.__init__(self, url, username, password)
