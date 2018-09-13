from user import User

def init_create_user():
    user = User()
    print()
    print("address:", user.address)
    print("key:", user.signing_key.to_string())
    print()
    print("Keep it secret, keep it safe")
