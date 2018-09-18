from plug.message import Event
from plug.registry import Registry

def register_transform_event(transform):
    registry = Registry().with_default()
    registry.register(Event)
    registry.register(transform)

    return registry
