from plug.key import ED25519SigningKey
from plug.util import plug_address

import aiohttp
import json
import asyncio

class User:
    def __init__(self):
        self.signing_key = ED25519SigningKey.new()
        self.address = plug_address(self.signing_key)
        self.nonce = 0

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
