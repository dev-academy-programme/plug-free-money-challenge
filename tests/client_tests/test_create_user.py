import pytest

from mocks.api_client import MockApiClient
from mocks.key_manager import MockKeyManager
from client.commands.create_user import init_create_user

def test_create_user_init_(mocker):
    mocker.patch('client.utils.PlugApiClient', MockApiClient)
    mocker.patch('client.utils.SqliteKeyManager', MockKeyManager)

    user = init_create_user()
    assert user.address == 'fake_address'
    assert user.network_id == 'fake_network_id'
