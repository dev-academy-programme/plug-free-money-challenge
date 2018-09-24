class MockKeyManager():
    def generate(self):
        return "fake_key"

    def set_nonce(self, address, network_id, nonce):
        return {
            address:address,
            network_id:network_id,
            nonce:nonce,
        }


def get_key_manager():
    return MockKeyManager()
