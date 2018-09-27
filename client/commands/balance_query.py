from free_money.model import BalanceModel
from asyncio import get_event_loop

def init_balance_query(client, address):
    loop = get_event_loop()
    response = loop.run_until_complete(client.get_model_instance(
        model=BalanceModel,
        key=address,
        height=-1,
    ))

    print("Your current balance is: " + str(response['balance']))
    return response
