
class MockApiClient():
    network_id = "fake_network_id"
    async def broadcast_transform(self, transform):
        return transform


def get_api_client():
    return MockApiClient()
