from key_manager import get_key_manager
from plug_api.clients.v1 import PlugApiClient

def get_api_client():
    # print(get_key_manager())
    return PlugApiClient("http://localhost:8181", get_key_manager())
