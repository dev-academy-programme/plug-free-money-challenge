from plug.key import ED25519SigningKey
from plug.util import plug_address

import aiohttp
import json
import asyncio

from plug_api.clients.v1 import PlugApiClient
from plug_api.key_managers.sqlite import SqliteKeyManager


class User:
    client = PlugApiClient("http://localhost:8181", "keys.db")
    def __init__(self):
        self.network_id = self.client.network_id
        self.key_manager = SqliteKeyManager('keys.db').setup()

        # key_manager = SqliteKeyManager("keys.db")
        self.address = self.key_manager.generate()
        # print(key_manager.__get_cursor)
        # print (key_manager.__contains__(self.address))
        # self.signing_key =
        # self.address = plug_address(self.signing_key)
        self.nonce = self.key_manager.set_nonce(self.address, self.network_id, 0)


    @staticmethod
    async def load(signing_key):
        signing_key = ED25519SigningKey.from_string(signing_key)
        user = User()
        user.signing_key = signing_key
        user.address = plug_address(signing_key)
        await user.get_nonce()
        return user

    async def get_nonce(self):
        async with aiohttp.ClientSession() as session:
            async with session.get("http://localhost:8181/_api/v1/state/-1/plug.model.NonceModel/" + self.address) as response:
                data = await response.json()
                self.nonce = data['value']
