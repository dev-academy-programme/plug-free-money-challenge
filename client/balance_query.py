from plug.key import ED25519SigningKey
import aiohttp

async def init_balance_query(address):
    async with aiohttp.ClientSession() as session:
        async with session.get("http://localhost:8181/_api/v1/state/-1/tutorial.BalanceModel/" + address) as response:
            data = await response.json()

    print(data)
