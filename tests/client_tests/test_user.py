import pytest

from client.user import User
from key_manager import MockKeyManager
from api_client import MockApiClient

def test_new_user_properties():
    """ARRANGE"""
    expected_address = "fake_key"
    expected_network_id = "fake_network_id"

    """ACT"""
    user = User(None)

    """ASSERT"""
    assert user.address == expected_address
    assert user.network_id == expected_network_id
    assert type(user.key_manager) is MockKeyManager
    assert type(user.client) is MockApiClient

def test_existing_user_properties():
    """ARRANGE"""
    existing_address = "fake_key"
    expected_network_id = "fake_network_id"

    """ACT"""
    user = User(existing_address)

    """ASSERT"""
    assert user.address == existing_address
    assert user.network_id == expected_network_id
    assert type(user.key_manager) is MockKeyManager
    assert type(user.client) is MockApiClient
