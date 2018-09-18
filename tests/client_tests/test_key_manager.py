import pytest
from client.key_manager import get_key_manager

def test_key_manager():
    expected_db_path = 'keys.db'

    key_manager = get_key_manager()

    assert key_manager.db_path == expected_db_path
