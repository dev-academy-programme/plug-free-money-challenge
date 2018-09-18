import pytest

from plug_api.clients.v1 import PlugApiClient
from client.api_client import get_api_client

def test_get_api_client():
    expected_network_id = "challenge.FreeMoney"
    client = get_api_client()

    assert client.network_id == expected_network_id
    assert type(client) == PlugApiClient
