from plug.key import ED25519SigningKey
from plug.hash import sha256
from plug.proof import SingleKeyProof
from balance_tutorial.transform import FreeMoney
from plug.transaction import Transaction
from plug.constant import TransactionEvent
from plug.message import Event
from plug.registry import Registry
import aiohttp
import asyncio
from balance_tutorial.user import User

async def main():
    registry = Registry().with_default()
    registry.register(Event)
    registry.register(FreeMoney)

    alice = User(ED25519SigningKey.new())

    transform = FreeMoney(
        receiver=alice.address,
        amount=1000,
    )

    challenge = transform.hash(sha256)
    proof = SingleKeyProof(alice.address, alice.nonce, challenge, 'balance.tutorial')
    proof.sign(alice.signing_key)
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
