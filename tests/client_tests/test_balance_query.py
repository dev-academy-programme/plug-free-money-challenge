import pytest
from pytest_mock import mocker

from api_client import MockApiClient
from free_money.model import BalanceModel

from client.balance_query import init_balance_query

def test_free_money_request_success(mocker):
    fake_address = "fake-address"
    client = MockApiClient()

    mocker.spy(client, 'get_model_instance')
    init_balance_query(client, fake_address)

    client.get_model_instance.assert_called_once()

    args = client.get_model_instance.call_args[1]

    assert args["height"] == -1
    assert args["key"] == fake_address
    assert args["model"] == BalanceModel
