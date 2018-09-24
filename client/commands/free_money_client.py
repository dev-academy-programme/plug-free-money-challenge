from plug.message import Event
from plug.registry import Registry

from client.register import register_transform_event

from free_money.transform import FreeMoney
from client.user import User

def init_free_money(client, address_input, amount):
    register_transform_event(FreeMoney)

    response = client.broadcast_transform(FreeMoney(
        receiver=address_input,
        amount=int(amount),
    ))

    print(response)
    return response
