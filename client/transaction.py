from plug.key import ED25519SigningKey
from plug.hash import sha256
from plug.proof import SingleKeyProof
from balance_tutorial.transform import BalanceTransfer
from plug.transaction import Transaction
from plug.constant import TransactionEvent
from plug.message import Event
from plug.registry import Registry
from balance_tutorial.user import User
import aiohttp
import asyncio
import json

async def init_transaction(sender_key_input, receiver_key_input, amount):
    registry = Registry().with_default()
    registry.register(Event)
    registry.register(BalanceTransfer)

    user_data = json.load(open("user_data.json", "r"))
    sender_user_obj = None
    receiver_user_obj = None

    for i, user in enumerate(user_data["users"]):
        if user_data["users"][i]["key"] == sender_key_input:
            user_data["users"][i]["nonce"] += 1;
            sender_user_obj = user_data["users"][i]
        if user_data["users"][i]["key"] == receiver_key_input:
            receiver_user_obj = user_data["users"][i]

    if sender_user_obj != None and receiver_user_obj != None:
        with open("user_data.json", "w") as write_file:
            json.dump(user_data, write_file)

    else:
        print("one or both of the user keys entered is invalid")
        return

    sender = User(ED25519SigningKey.from_string(sender_user_obj["key"]))
    receiver = User(ED25519SigningKey.from_string(receiver_user_obj["key"]))

    transform = BalanceTransfer(
        sender=sender.address,
        receiver=receiver.address,
        amount=int(amount),
    )

    challenge = transform.hash(sha256)
    proof = SingleKeyProof(sender.address, sender_user_obj["nonce"], challenge, 'balance.tutorial')
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
