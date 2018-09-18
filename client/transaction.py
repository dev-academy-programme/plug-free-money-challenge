from free_money.transform import BalanceTransfer

from client.api_client import get_api_client
from register import register_transform_event

from user import User

async def init_transaction(sender_key_input, receiver_address, amount):
    register_transform_event(BalanceTransfer)

    response = get_api_client().broadcast_transform(BalanceTransfer(
        sender=sender_key_input,
        receiver=receiver_address,
        amount=int(amount)
    ))

    print(response)
