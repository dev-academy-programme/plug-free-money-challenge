import pytest
from pytest_mock import mocker
import mock

from client.register import register_transform_event
from plug.message import Event
import plug.registry


class FakeTransform():
    fqdn = 'fake.transform'

def test_register_transform():
    registry = register_transform_event(FakeTransform)

    saved_transform = registry._fqdns['fake.transform']
    saved_event = registry._fqdns[Event.fqdn]

    assert type(registry) is plug.registry.Registry
    assert saved_transform is FakeTransform
    assert saved_event is Event
