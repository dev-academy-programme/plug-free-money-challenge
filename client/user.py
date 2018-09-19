from plug_api.clients.v1 import PlugApiClient
from plug_api.key_managers.sqlite import SqliteKeyManager

from api_client import get_api_client
from key_manager import get_key_manager

class User:
    client = get_api_client()
    key_manager = get_key_manager()
    network_id = client.network_id

    def __init__(self, address):
        if (address):
            self.address = address
        else:
            self.address = self.key_manager.generate()
            self.key_manager.set_nonce(self.address, self.network_id, 0)
