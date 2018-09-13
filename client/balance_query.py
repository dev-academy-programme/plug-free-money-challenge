from plug.key import ED25519SigningKey
from plug.hash import sha256
from plug.proof import SingleKeyProof
from balance_tutorial.transform import BalanceQuery
from plug.transaction import Transaction
from plug.constant import TransactionEvent
from plug.message import Event
from plug.registry import Registry
import aiohttp
import json
import asyncio
from balance_tutorial.user import User

async def init_balance_query(signing_key_input):

    user = User(ED25519SigningKey.from_string(signing_key_input))

    async with aiohttp.ClientSession() as session:
        async with session.get("http://localhost:8181/_api/v1/state/-1/tutorial.BalanceModel/" + user.address) as response:
            data = await response.json()

    print(data)
