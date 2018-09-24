from client.utils import get_api_client, get_key_manager

class User:

    def __init__(self, address):
        self.client = get_api_client()
        self.key_manager = get_key_manager()
        self.network_id = self.client.network_id

        if (address):
            self.address = address
        else:
            self.address = self.key_manager.generate()
            self.key_manager.set_nonce(self.address, self.network_id, 0)
