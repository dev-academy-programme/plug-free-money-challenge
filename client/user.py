from plug_api.clients.v1 import PlugApiClient
from plug_api.key_managers.sqlite import SqliteKeyManager

class User:
    client = PlugApiClient("http://localhost:8181", "keys.db")
    network_id = client.network_id
    key_manager = SqliteKeyManager('keys.db').setup()

    def __init__(self, address):
        if (address):
            self.address = address
        else:
            self.address = key_manager.generate()
            key_manager.set_nonce(self.address, network_id, 0)

    @staticmethod
    async def load(address):
        user = User(address)
        user.nonce = await user.get_nonce()
        return user

    async def get_nonce(self):
        return self.key_manager.get_nonce(self.address, self.network_id)
