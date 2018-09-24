import pytest
from pytest_mock import mocker

from mocks.api_client import MockApiClient
from free_money.transform import BalanceTransfer

from client.transaction import init_transaction

def test_transaction_request_success(mocker):
    sender_address = "fake-sender"
    receiver_address = "fake-receiver"
    amount = 100
    client = MockApiClient()

    mocker.spy(client, 'broadcast_transform')
    
    init_transaction(client, sender_address, receiver_address, amount)

    client.broadcast_transform.assert_called_once()

    broadcasted_transform = client.broadcast_transform.call_args[0][0]
    assert type(broadcasted_transform) is BalanceTransfer
    assert broadcasted_transform.amount == amount
    assert broadcasted_transform.receiver == receiver_address
    assert broadcasted_transform.sender == sender_address
