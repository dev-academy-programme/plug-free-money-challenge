from plug_api.key_managers.sqlite import SqliteKeyManager

def get_key_manager():
    return SqliteKeyManager('keys.db').setup()
