from plug.message import Event
from plug.registry import Registry

from register import register_transform_event

from free_money.transform import FreeMoney
from user import User

async def init_free_money(client, address_input, amount):
    register_transform_event(FreeMoney)

    response = await client.broadcast_transform(FreeMoney(
        receiver=address_input,
        amount=int(amount),
    ))

    print(response)
    return response
