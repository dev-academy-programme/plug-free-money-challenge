from free_money.transform import BalanceTransfer

from register import register_transform_event

from user import User

def init_transaction(client, sender_key_input, receiver_address, amount):
    register_transform_event(BalanceTransfer)

    response = client.broadcast_transform(BalanceTransfer(
        sender=sender_key_input,
        receiver=receiver_address,
        amount=int(amount)
    ))

    print(response)
