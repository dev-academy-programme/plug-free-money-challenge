from plug.key import ED25519SigningKey
from plug.util import plug_address

import aiohttp
import json
import asyncio

from plug_api.clients.v1 import PlugApiClient
from plug_api.key_managers.sqlite import SqliteKeyManager

class User:
    def __init__(self, address):
        client = PlugApiClient("http://localhost:8181", "keys.db")
        network_id = client.network_id
        key_manager = SqliteKeyManager('keys.db').setup()

        # key_manager = SqliteKeyManager("keys.db")
        if (address):
            self.address = address
        else:
            self.address = key_manager.generate()
            key_manager.set_nonce(self.address, network_id, 0)

        # print(key_manager.__get_cursor)
        # print (key_manager.__contains__(self.address))
        # self.signing_key =
        # self.address = plug_address(self.signing_key)
        # self.nonce =


    @staticmethod
    async def load(address):
        client = PlugApiClient("http://localhost:8181", "keys.db")
        network_id = client.network_id
        key_manager = SqliteKeyManager('keys.db').setup()
        # signing_key = ED25519SigningKey.from_string(signing_key)
        user = User(address)
        # user.address = plug_address(signing_key)
        nonce = key_manager.increment_nonce(address, network_id)
        print(nonce)
        # await user.get_nonce()
        return user

    async def get_nonce(self):
        async with aiohttp.ClientSession() as session:
            async with session.get("http://localhost:8181/_api/v1/state/-1/plug.model.NonceModel/" + self.address) as response:
                data = await response.json()
                self.nonce = data['value']
