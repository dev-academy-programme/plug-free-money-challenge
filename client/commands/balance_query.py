from free_money.model import BalanceModel

def init_balance_query(client, address):
    response = client.get_model_instance(
        model=BalanceModel,
        key=address,
        height=-1,
    )
    print("Your current balance is: " + str(response['balance']))
    return response
