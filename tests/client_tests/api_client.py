
class MockApiClient():
    network_id = "fake_network_id"
    async def broadcast_transform(self, transform):
        return transform
    async def get_model_instance(self, model, key, height):
        return {
            "balance":100,
        }


def get_api_client():
    return MockApiClient()
