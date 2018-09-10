import asyncio
from create_user import main

def create_user():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())

create_user()
