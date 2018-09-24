class MockKeyManager():
    def __init__(self, file='keys.db'):
        return 

    def setup(self):
        return self

    def generate(self):
        return "fake_address"

    def set_nonce(self, address, network_id, nonce):
        return {
            address:address,
            network_id:network_id,
            nonce:nonce,
        }


def get_key_manager():
    return MockKeyManager()
