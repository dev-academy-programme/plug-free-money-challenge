import click
import asyncio
from freemoney import main

@click.command()
@click.option('--signing_key', prompt='Enter a user signing key',
              help='The person to get free money.')
def attempt_free_money(signing_key):
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(signing_key))

if __name__ == '__main__':
    attempt_free_money()
