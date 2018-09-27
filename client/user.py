from client.utils import get_api_client, get_key_manager
from asyncio import get_event_loop

class User:

    def __init__(self, address):
        self.client = get_api_client()
        self.key_manager = get_key_manager()

        loop = get_event_loop()
        self.network_id = loop.run_until_complete(self.client.get_network_id())

        if (address):
            self.address = address
        else:
            self.address = self.key_manager.generate()
            self.key_manager.set_nonce(self.address, self.network_id, 0)
