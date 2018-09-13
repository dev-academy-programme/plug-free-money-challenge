from plug.hash import sha256
from plug.proof import SingleKeyProof
from balance_tutorial.transform import BalanceTransfer
from plug.transaction import Transaction
from plug.constant import TransactionEvent
from plug.message import Event
from plug.registry import Registry
from user import User
import aiohttp
import asyncio
import json

async def init_transaction(sender_key_input, receiver_address, amount):
    registry = Registry().with_default()
    registry.register(Event)
    registry.register(BalanceTransfer)

    user_data = json.load(open("user_data.json", "r"))

    sender = await User.load(sender_key_input)

    transform = BalanceTransfer(
        sender=sender.address,
        receiver=receiver_address,
        amount=int(amount),
    )

    challenge = transform.hash(sha256)
    proof = SingleKeyProof(sender.address, sender.nonce, challenge, 'balance.tutorial')
    proof.sign(sender.signing_key)
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
