from plug.key import ED25519SigningKey
from plug.hash import sha256
from plug.proof import SingleKeyProof
from balance_tutorial.transform import FreeMoney
from plug.transaction import Transaction
from plug.constant import TransactionEvent
from plug.message import Event
from plug.registry import Registry
from user import User
import aiohttp
import json
import asyncio

async def init_free_money(signing_key_input):
    registry = Registry().with_default()
    registry.register(Event)
    registry.register(FreeMoney)

    user = await User.load(signing_key_input)

    transform = FreeMoney(
        receiver=user.address,
        amount=1000,
    )

    challenge = transform.hash(sha256)
    proof = SingleKeyProof(user.address, user.nonce, challenge, 'balance.tutorial')
    proof.sign(user.signing_key)
    transaction = Transaction(transform, {proof.address: proof})

    event = Event(
        event=TransactionEvent.ADD,
        payload=transaction
    )

    payload = registry.pack(event)

    async with aiohttp.ClientSession() as session:
        async with session.post("http://localhost:8181/_api/v1/transaction", json=payload) as response:
            data = await response.json()

    print(data)
