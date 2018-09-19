from free_money.model import BalanceModel

async def init_balance_query(client, address):
    response = await client.get_model_instance(
        model=BalanceModel,
        key=address,
        height=-1,
    )
    print("Your current balance is: " + str(response['balance']))
    return response
