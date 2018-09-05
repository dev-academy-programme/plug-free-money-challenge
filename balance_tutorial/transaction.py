from plug.key import ED25519SigningKey
from plug.util import plug_address
from plug.hash import sha256
# from hashlib import sha256
from plug.proof import SingleKeyProof
from transform import BalanceTransfer
from plug.transaction import Transaction
from plug.constant import TransactionEvent
from plug.message import Event
from plug.registry import Registry
import aiohttp
import asyncio

class User:
    def __init__(self, signing_key):
        self.signing_key = signing_key
        self.nonce = 0
        self.address = plug_address(signing_key)

async def main():
    registry = Registry().with_default()
    registry.register(Event)
    registry.register(BalanceTransfer)

    bob = User(ED25519SigningKey.new())
    alice = User(ED25519SigningKey.new())

    transform = BalanceTransfer(
        sender=bob.address,
        receiver=alice.address,
        amount=10,
    )

    challenge = transform.hash(sha256)
    print(challenge)
    proof = SingleKeyProof(bob.address, bob.nonce, challenge, "1")
    proof.sign(bob.signing_key)
    print(proof)
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

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
