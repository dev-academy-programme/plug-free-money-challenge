from plug.message import Event
from plug.registry import Registry
from plug_api.key_managers.sqlite import SqliteKeyManager
from plug_api.clients.v1 import PlugApiClient

def register_transform_event(transform):
    registry = Registry().with_default()
    registry.register(Event)
    registry.register(transform)
    return registry


def get_key_manager():
    return SqliteKeyManager('keys.db').setup()

def get_api_client():
    return PlugApiClient("http://localhost:8181", get_key_manager())
