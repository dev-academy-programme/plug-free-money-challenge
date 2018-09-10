from plug.key import ED25519SigningKey
from plug.hash import sha256
from plug.proof import SingleKeyProof
from balance_tutorial.transform import FreeMoney
from plug.transaction import Transaction
from plug.constant import TransactionEvent
from plug.message import Event
from plug.registry import Registry
import aiohttp
import json
import asyncio
from balance_tutorial.user import User

async def main(signing_key_input):
    registry = Registry().with_default()
    registry.register(Event)
    registry.register(FreeMoney)

    user_data = json.load(open("user_data.json", "r"))
    user_obj = None

    for i, user in enumerate(user_data["users"]):
        if user_data["users"][i]["key"] == signing_key_input:
            user_data["users"][i]["nonce"] += 1;
            user_obj = user_data["users"][i]
            with open("user_data.json", "w") as write_file:
                json.dump(user_data, write_file)

    if user_obj == None:
        print("no user found with that key")
        return

    user = User(ED25519SigningKey.from_string(signing_key_input))

    transform = FreeMoney(
        receiver=user.address,
        amount=1000,
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

# loop = asyncio.get_event_loop()
# loop.run_until_complete(main())
