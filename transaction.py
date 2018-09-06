from plug.constant import TransactionEvent
from plug.key import ED25519SigningKey
from plug.message import Event
from plug.proof import SingleKeyProof
from plug.registry import Registry
from plug.transaction import Transaction
from plug.util import plug_address
from plug.hash import sha256
from balance_tutorial.transform import BalanceTransfer
import asyncio
import aiohttp
import time

class User:
    def __init__(self, signing_key):
        self.signing_key = signing_key
        self.address = plug_address(signing_key)

async def main():
    registry = Registry().with_default()
    registry.register(Event)
    registry.register(BalanceTransfer)

    bob = User(ED25519SigningKey.new())
    alice = User(ED25519SigningKey.new())
    nonce = round(time.time() * 100)

    transform = BalanceTransfer(
        sender=bob.address,
        receiver=alice.address,
        amount=10,
    )

    challenge = transform.hash(sha256)

    proof = SingleKeyProof(bob.address, nonce, challenge, 'balance.tutorial')
    proof.sign(bob.signing_key)

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

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
