import pytest
from uuid import uuid4

from plug.registry import Registry
from plug_api.key_managers.base import KeyManager

from free_money.model import BalanceModel
from free_money.transform import FreeMoney, BalanceTransfer

# from plug.error import MissingAuthorizationsError
# from plug.transaction import Transaction
from plug_api.testing import authenticate_transaction, create_state, \
    execute_transform, verify_transform
#
# from trackback.exceptions import AddressMismatch, AlreadyDelivered, \
#     ConsignmentDoesNotExist, InvalidParameters

def test_test():
    assert 1 == 1

def test_balance_transfer_success(
        dapp_registry: Registry,
        key_manager: KeyManager,
):
    """
    Recording successful delivery; no violations occurred during
    shipment.
    """
    sender_address = key_manager.generate()
    receiver_address = key_manager.generate()
    send_amount = 100
    what_is_this_id = str(uuid4())
    # escrow_amount = 100

    transform = BalanceTransfer(
        sender=sender_address,
        receiver=receiver_address,
        amount=send_amount,
    )

    # Initialize the environment.
    state = create_state(dapp_registry)

    balance_state = state[BalanceModel.fqdn]

    balance_state[sender_address] = BalanceModel(
        balance=100
    )

    balance_state[receiver_address] = BalanceModel(
        balance=100
    )

    execute_transform(transform, state)

    the_receiver: BalanceModel = balance_state[receiver_address]
    the_sender: BalanceModel = balance_state[sender_address]

    assert the_receiver.balance == 200
    assert the_sender.balance == 0

def test_free_money_success(
        dapp_registry: Registry,
        key_manager: KeyManager,
):
    """
    Recording successful delivery; no violations occurred during
    shipment.
    """
    receiver_address = key_manager.generate()
    free_money_amount = 100
    what_is_this_id = str(uuid4())
    # escrow_amount = 100

    transform = FreeMoney(
        receiver=receiver_address,
        amount=free_money_amount,
    )

    # Initialize the environment.
    state = create_state(dapp_registry)

    state[BalanceModel.fqdn][receiver_address] = BalanceModel(
        balance=100
    )

    execute_transform(transform, state)

    the_receiver: BalanceModel = state[BalanceModel.fqdn][receiver_address]
    print(the_receiver)
    assert the_receiver.balance == 200
