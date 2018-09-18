import pytest
from pytest_mock import mocker
import mock

from client.register import register_transform_event
import plug.message
import plug.registry


class FakeTransform():
    fqdn = 'fake.transform'

def test_register_transform():

    # plug.message.Event = FakeEvent
    registry = register_transform_event(FakeTransform)

    assert type(registry) is plug.registry.Registry
    # assert registry.transform_fqdns == 1
