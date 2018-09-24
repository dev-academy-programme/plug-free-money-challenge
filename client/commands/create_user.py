from client.user import User

def init_create_user():
    user = User(None)
    print()
    print("address/key:", user.address)
    print()
    print("Keep it secret, keep it safe")
    return user
