import pytest

from uuid import uuid4

from plug.registry import Registry
from plug_api.key_managers.base import KeyManager
from plug_api.testing import authenticate_transaction, create_state, \
    execute_transform, verify_transform

from free_money.model import BalanceModel
from free_money.transform import FreeMoney, BalanceTransfer
from free_money.error import InvalidAmountError, NotEnoughMoneyError

def test_balance_transfer_success(
        dapp_registry: Registry,
        key_manager: KeyManager,
):
    """
    ARRANGE
    """
    #Define fake values for the transform
    sender_address = key_manager.generate()
    sender_initial_balance=100
    receiver_address = key_manager.generate()
    receiver_initial_balance=100
    send_amount = 100
    what_is_this_id = str(uuid4())

    ##Build the Transform
    transform = BalanceTransfer(
        sender=sender_address,
        receiver=receiver_address,
        amount=send_amount,
    )

    #Create a fake state
    state = create_state(dapp_registry)


    balance_state = state[BalanceModel.fqdn]
    #Set Initial Balance for Sender
    balance_state[sender_address] = BalanceModel(
        balance=sender_initial_balance
    )
    #Set Inital Balance for receiver
    balance_state[receiver_address] = BalanceModel(
        balance=receiver_initial_balance
    )

    """
    ACT
    """
    #Run the Transform
    execute_transform(transform, state)

    #Define the balance models of the sender and receiver
    the_receiver: BalanceModel = balance_state[receiver_address]
    the_sender: BalanceModel = balance_state[sender_address]

    """
    ASSERT
    """
    assert the_receiver.balance == receiver_initial_balance+send_amount
    assert the_sender.balance == sender_initial_balance-send_amount

def test_balance_transfer_zero_money_error(
        dapp_registry: Registry,
        key_manager: KeyManager,
):
    """
    ARRANGE
    """
    #Define fake values for the transform
    sender_address = key_manager.generate()
    sender_initial_balance=100
    receiver_initial_balance=100
    receiver_address = key_manager.generate()
    send_amount = 0
    what_is_this_id = str(uuid4())

    ##Build the Transform
    transform = BalanceTransfer(
        sender=sender_address,
        receiver=receiver_address,
        amount=send_amount,
    )

    #Create a fake state
    state = create_state(dapp_registry)


    balance_state = state[BalanceModel.fqdn]
    #Set Initial Balance for Sender
    balance_state[sender_address] = BalanceModel(
        balance=sender_initial_balance
    )
    #Set Inital Balance for receiver
    balance_state[receiver_address] = BalanceModel(
        balance=receiver_initial_balance
    )

    """
    ACT
    """
    #Run the Transform
    with pytest.raises(InvalidAmountError):
        execute_transform(transform, state)

    #Define the balance models of the sender and receiver
    the_receiver: BalanceModel = balance_state[receiver_address]
    the_sender: BalanceModel = balance_state[sender_address]

    """
    ASSERT
    """
    assert the_receiver.balance == receiver_initial_balance
    assert the_sender.balance == sender_initial_balance

def test_balance_transfer_not_enough_money_error(
        dapp_registry: Registry,
        key_manager: KeyManager,
):
    """
    ARRANGE
    """
    #Define fake values for the transform
    sender_address = key_manager.generate()
    receiver_address = key_manager.generate()
    sender_initial_balance=99
    receiver_initial_balance=100
    send_amount = 100
    what_is_this_id = str(uuid4())

    ##Build the Transform
    transform = BalanceTransfer(
        sender=sender_address,
        receiver=receiver_address,
        amount=send_amount,
    )

    #Create a fake state
    state = create_state(dapp_registry)


    balance_state = state[BalanceModel.fqdn]
    #Set Initial Balance for Sender
    balance_state[sender_address] = BalanceModel(
        balance=sender_initial_balance
    )
    #Set Inital Balance for receiver
    balance_state[receiver_address] = BalanceModel(
        balance=receiver_initial_balance
    )

    """
    ACT
    """
    #Run the Transform
    with pytest.raises(NotEnoughMoneyError):
        execute_transform(transform, state)

    #Define the balance models of the sender and receiver
    the_receiver: BalanceModel = balance_state[receiver_address]
    the_sender: BalanceModel = balance_state[sender_address]

    """
    ASSERT
    """
    assert the_receiver.balance == receiver_initial_balance
    assert the_sender.balance == sender_initial_balance

def test_free_money_success(
        dapp_registry: Registry,
        key_manager: KeyManager,
):
    """
    ARRANGE
    """
    receiver_address = key_manager.generate()
    receiver_initial_balance=100
    free_money_amount = 100
    what_is_this_id = str(uuid4())

    transform = FreeMoney(
        receiver=receiver_address,
        amount=free_money_amount,
    )

    # Initialize the environment.
    state = create_state(dapp_registry)

    balance_state = state[BalanceModel.fqdn]

    balance_state[receiver_address] = BalanceModel(
        balance=receiver_initial_balance
    )

    """
    ACT
    """
    execute_transform(transform, state)

    the_receiver: BalanceModel = balance_state[receiver_address]

    """
    ASSERT
    """
    assert the_receiver.balance == receiver_initial_balance+free_money_amount

def test_free_zero_money_error(
        dapp_registry: Registry,
        key_manager: KeyManager,
):
    """
    ARRANGE
    """
    receiver_address = key_manager.generate()
    receiver_initial_balance=100
    free_money_amount = 0
    what_is_this_id = str(uuid4())

    transform = FreeMoney(
        receiver=receiver_address,
        amount=free_money_amount,
    )

    # Initialize the environment.
    state = create_state(dapp_registry)

    balance_state = state[BalanceModel.fqdn]

    balance_state[receiver_address] = BalanceModel(
        balance=receiver_initial_balance
    )

    """
    ACT
    """
    with pytest.raises(InvalidAmountError):
        execute_transform(transform, state)

    the_receiver: BalanceModel = balance_state[receiver_address]

    """
    ASSERT
    """
    assert the_receiver.balance == receiver_initial_balance
