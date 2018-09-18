from plug.message import Event
from plug.registry import Registry

from plug_api.clients.v1 import PlugApiClient
from plug_api.key_managers.sqlite import SqliteKeyManager

from free_money.transform import FreeMoney
from user import User

async def init_free_money(address_input):
    registry = Registry().with_default()
    registry.register(Event)
    registry.register(FreeMoney)

    key_manager = SqliteKeyManager('keys.db').setup()
    client = PlugApiClient("http://localhost:8181", key_manager)

    response = client.broadcast_transform(FreeMoney(
        receiver=address_input,
        amount=1000,
    ))

    print(response)
