from plug.message import Event
from plug.registry import Registry

from client.api_client import get_api_client
from register import register_transform_event

from free_money.transform import FreeMoney
from user import User

async def init_free_money(address_input, amount):
    register_transform_event(FreeMoney)

    response = get_api_client().broadcast_transform(FreeMoney(
        receiver=address_input,
        amount=int(amount),
    ))

    print(response)
