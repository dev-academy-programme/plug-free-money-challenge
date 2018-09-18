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

    print(user)

    transform = FreeMoney(
        receiver=user.address,
        amount=1000,
    )

    key_manager = SqliteKeyManager('keys.db')
    key_manager.setup()


    key_manager = SqliteKeyManager('keys.db').setup()
    client = PlugApiClient("http://localhost:8181", key_manager)

    # client = PlugApiClient("http://localhost:8181", "keys.db")
    client.broadcast_transform(transform)
    await user.increment_nonce()
    # actual_response = api_client.broadcast_transform(
    #     transform=transform,
    #     sync_nonces=True,
    # )
    #
    # print(actual_response)


    # challenge = transform.hash(sha256)
    # proof = SingleKeyProof(user.address, user.nonce, challenge, 'challenge.FreeMoney')
    # proof.sign(user.signing_key)
    # transaction = Transaction(transform, {proof.address: proof})
    #
    # event = Event(
    #     event=TransactionEvent.ADD,
    #     payload=transaction
    # )
    #
    # payload = registry.pack(event)
    #
    # async with aiohttp.ClientSession() as session:
    #     async with session.post("http://localhost:8181/_api/v1/transaction", json=payload) as response:
    #         data = await response.json()

    # print(data)
