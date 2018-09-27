
class MockApiClient():
    def __init__(self, url='test', key_manager=None):
        return

    async def get_network_id(self):
        return "fake_network_id"

    async def broadcast_transform(self, transform):
        return transform

    async def get_model_instance(self, model, key, height):
        return {
            "balance":100,
        }


def get_api_client():
    return MockApiClient()
