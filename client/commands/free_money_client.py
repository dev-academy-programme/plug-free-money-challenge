from free_money.transform import FreeMoney
from client.utils import register_transform_event
from client.user import User

from asyncio import get_event_loop

async def init_free_money(client, address_input, amount):
    register_transform_event(FreeMoney)

    loop = get_event_loop()

    response = loop.run_until_complete(client.broadcast_transform(FreeMoney(
        receiver=address_input,
        amount=int(amount),
    )))

    print(response)
    return response
