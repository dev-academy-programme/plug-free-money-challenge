from plug_api.clients.v1 import PlugApiClient
from plug_api.key_managers.sqlite import SqliteKeyManager

from free_money.model import BalanceModel

async def init_balance_query(address):
    key_manager = SqliteKeyManager('keys.db').setup()
    client = PlugApiClient("http://localhost:8181", key_manager)

    response = client.get_model_instance(
        model=BalanceModel,
        key=address,
        height=-1,
    )

    print("Your current balance is: " + str(response['balance']))
