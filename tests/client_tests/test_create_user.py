import pytest

from client.create_user import init_create_user
from user import get_mock_user

def test_create_user_init_():
    expected_address = "fake_address"
    expected_type = type(get_mock_user())

    user = init_create_user()
    assert type(user) is expected_type
    assert user.address == expected_address
