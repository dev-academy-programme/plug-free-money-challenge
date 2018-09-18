class User():
    address = "fake_address"
    def __init__(self, address):
        print(self.address)
        return None



def get_mock_user():
    return User(None)
