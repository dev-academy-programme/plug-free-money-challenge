from plug.key import ED25519SigningKey
from plug.hash import sha256
from plug.proof import SingleKeyProof
from free_money.transform import FreeMoney
from plug.transaction import Transaction
from plug.constant import TransactionEvent
from plug.message import Event
from plug.registry import Registry
from user import User
import aiohttp
import json
import asyncio

from plug_api.clients.v1 import PlugApiClient
from plug_api.key_managers.sqlite import SqliteKeyManager


async def init_free_money(address_input):
    registry = Registry().with_default()
    registry.register(Event)
    registry.register(FreeMoney)

    user = await User.load(address_input)
    key_manager = SqliteKeyManager('keys.db').setup()
    client = PlugApiClient("http://localhost:8181", key_manager)

    transform = FreeMoney(
        receiver=address_input,
        amount=1000,
    )

    response = client.broadcast_transform(transform)
    print(response)
