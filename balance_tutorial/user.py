from plug.util import plug_address

class User:
    def __init__(self, signing_key):
        self.signing_key = signing_key
        self.nonce = 0
        self.address = plug_address(signing_key)
