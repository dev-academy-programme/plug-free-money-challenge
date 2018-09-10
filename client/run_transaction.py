import click
import asyncio
from transaction import main

@click.command()
@click.option('--sender_signing_key', prompt='Enter the sender signing key',
              help='The person to give money.')
@click.option('--receiver_signing_key', prompt='Enter the receiver signing key',
              help='The person to get money.')
@click.option('--amount', prompt='Enter the amount to transfer',
              help='The person to get money.')
def attempt_transaction(sender_signing_key, receiver_signing_key, amount):
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(sender_signing_key, receiver_signing_key, amount))

if __name__ == '__main__':
    attempt_transaction()
