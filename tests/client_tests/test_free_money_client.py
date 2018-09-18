import pytest
from pytest_mock import mocker
import asyncio

from api_client import MockApiClient
from free_money.transform import FreeMoney

from client.free_money_client import init_free_money

def test_free_money_request_success(mocker):
    fake_address = "fake-address"
    amount = 100
    client = MockApiClient()

    mocker.spy(client, 'broadcast_transform')
    loop = asyncio.get_event_loop()
    loop.run_until_complete(init_free_money(client, fake_address, amount))

    client.broadcast_transform.assert_called_once()

    broadcasted_transform = client.broadcast_transform.call_args[0][0]
    assert type(broadcasted_transform) is FreeMoney
    assert broadcasted_transform.amount == amount
    assert broadcasted_transform.receiver == fake_address
