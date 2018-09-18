from plug.message import Event
from plug.registry import Registry
from user import User

from plug.message import Event
from plug.registry import Registry

from plug_api.clients.v1 import PlugApiClient
from plug_api.key_managers.sqlite import SqliteKeyManager

from free_money.transform import BalanceTransfer
from user import User


async def init_transaction(sender_key_input, receiver_address, amount):
    registry = Registry().with_default()
    registry.register(Event)
    registry.register(BalanceTransfer)

    # sender = await User.load(sender_key_input)

    key_manager = SqliteKeyManager('keys.db').setup()
    client = PlugApiClient("http://localhost:8181", key_manager)

    response = client.broadcast_transform(BalanceTransfer(
        sender=sender_key_input,
        receiver=receiver_address,
        amount=int(amount)
    ))

    print(response)
