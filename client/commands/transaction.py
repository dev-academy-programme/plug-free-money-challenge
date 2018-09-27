from free_money.transform import BalanceTransfer
from asyncio import get_event_loop

from client.utils import register_transform_event
from client.user import User

def init_transaction(client, sender_key_input, receiver_address, amount):
    register_transform_event(BalanceTransfer)

    loop = get_event_loop()

    response = loop.run_until_complete(client.broadcast_transform(BalanceTransfer(
        sender=sender_key_input,
        receiver=receiver_address,
        amount=int(amount)
    )))

    print(response)
