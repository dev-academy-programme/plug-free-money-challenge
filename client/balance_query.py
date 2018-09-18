from free_money.model import BalanceModel
from client.api_client import get_api_client

async def init_balance_query(address):
    response = get_api_client().get_model_instance(
        model=BalanceModel,
        key=address,
        height=-1,
    )
    print("Your current balance is: " + str(response['balance']))
