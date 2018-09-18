from create_user import init_create_user
from balance_query import init_balance_query
from free_money_client import init_free_money
from transaction import init_transaction
import click
import asyncio

@click.command()
@click.argument('arg')
def init(arg):
    if arg == 'balance_query':
        input_address = click.prompt("please enter a user address",)
        loop = asyncio.get_event_loop()
        loop.run_until_complete(init_balance_query(input_address))
        return

    if arg == 'create_user':
        init_create_user()
        return

    if arg == 'free_money':
        input_key = click.prompt("please enter a user signing key",)
        amount = click.prompt("please enter the amount",)
        loop = asyncio.get_event_loop()
        loop.run_until_complete(init_free_money(input_key, amount))
        return

    if arg == 'transaction':
        sender_input_key = click.prompt("please enter the sender signing key",)
        receiver_address = click.prompt("please enter the receiver address",)
        amount = click.prompt("please enter the amount",)
        loop = asyncio.get_event_loop()
        loop.run_until_complete(init_transaction(sender_input_key, receiver_address, amount))
        return

    else:
        print("Error: Invalid Argument")

if __name__ == '__main__':
    init()
