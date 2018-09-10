from plug.key import ED25519SigningKey
from plug.hash import sha256
from plug.proof import SingleKeyProof
from balance_tutorial.transform import CreateUser
from plug.transaction import Transaction
from plug.constant import TransactionEvent
from plug.message import Event
from plug.registry import Registry
from balance_tutorial.user import User
import aiohttp
import json
import asyncio

async def main():
    registry = Registry().with_default()
    registry.register(Event)
    registry.register(CreateUser)

    user_obj = {"key" : ED25519SigningKey.to_string(ED25519SigningKey.new()), "nonce" : 0}
    user = User(ED25519SigningKey.from_string(user_obj["key"]))

    user_data = json.load(open("user_data.json", "r"))
    user_data["users"].append(user_obj)

    with open("user_data.json", "w") as write_file:
        json.dump(user_data, write_file)

    transform = CreateUser(
        user=user.address,
    )

    challenge = transform.hash(sha256)
    proof = SingleKeyProof(user.address, user_obj["nonce"], challenge, 'balance_tutorial')
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
