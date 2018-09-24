import click
import asyncio

from commands.create_user import init_create_user
from commands.balance_query import init_balance_query
from commands.free_money_client import init_free_money
from commands.transaction import init_transaction

from api_client import get_api_client

@click.command()
@click.argument('arg')
def init(arg):
    client = get_api_client()
    if arg == 'balance_query':
        input_address = click.prompt("please enter a user address",)
        init_balance_query(client, input_address)
        return

    if arg == 'create_user':
        init_create_user()
        return

    if arg == 'free_money':
        input_key = click.prompt("please enter a user signing key",)
        amount = click.prompt("please enter the amount",)
        init_free_money(client, input_key, amount)
        return

    if arg == 'transaction':
        sender_input_key = click.prompt("please enter the sender signing key",)
        receiver_address = click.prompt("please enter the receiver address",)
        amount = click.prompt("please enter the amount",)
        init_transaction(client, sender_input_key, receiver_address, amount)
        return

    else:
        print("Error: Invalid Argument")

if __name__ == '__main__':
    init()
