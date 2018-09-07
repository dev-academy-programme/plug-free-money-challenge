import click
import asyncio
from balance_query import main

@click.command()
@click.option('--signing_key', prompt='Enter a user signing key',
              help='The user to query.')
def query_balance(signing_key):
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(signing_key))

if __name__ == '__main__':
    query_balance()
