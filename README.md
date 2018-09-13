Balance Tutorial
==============================

## INTRODUCTION TO PLUG AND TRANSFORMS

### OBJECTIVES
- Create a function that adds a new user to the blockchain.
- Create a function that can query the balance of a specific User.
- Create a Transform that adds free money to a specific Users balance.
- Create a Transform that can transfer money between two Users

#### OBJECTIVE: CREATING A USER.

##### Step One: Writing the User class in `user.py`.

The first step in creating a new User takes place over in `user.py`. There are three methods in here that need fleshing out.

First, the `__init__(self)` method must define some properties of this new User class. The user `signing_key`, `address` and `nonce` must all be defined.  

Next, the `load(signing_key)` method: it must be able to take a new `signing_key` argument, create a new instance of the User class, assign its properties, then return the new user object.

Finally, we need a function to get the current nonce of the User. Read the API docs on issuing GET requests on the NonceModel. IE: `http://localhost:8181/_api/v1/state/-1/plug.model.NonceModel/ ... `.

##### Step Two: Writing the client code in `create_user.py`.

Write the `_init_create_user()` function in `create_user.py`. This is an extremely brief operation. Simply create a new `User()` instance using the code you wrote in `user.py`, and log all the User info into the terminal. 

```
@dataclass
class CreateUser(Transform):
    fqdn = "tutorial.CreateUser"
    user: str

    def required_authorizations(self):
        return {self.user}

    @staticmethod
    def required_models():
        return {BalanceModel.fqdn}

    def required_keys(self):
        return {self.user}

    @staticmethod
    def pack(registry, obj):
        return {
            "user": obj.user,
        }

    @classmethod
    def unpack(cls, registry, payload):
        return cls(
            user=payload["user"],
        )

    def verify(self, state_slice):
        print("verify")

    def apply(self, state_slice):
        print('-----------')
        print('NEW USER CREATED!')
        print('-----------')

```

When applied, this Transform will create a new User and display some confirmation text in the server log.

#### STEP 2: Add the new Transform as a Plugin component in `__init__.py`

Whenever you create a new transform you must remember to add it it into the components array in your Plugin class. This is done in the `__init__.py` file:

```
from plug.abstract import Plugin

import balance_tutorial.error
import balance_tutorial.model
import balance_tutorial.transform

class BalanceTutorialPlugin(Plugin):
    @classmethod
    def setup(cls, registry):
        components = [
            # Include your plugin's models/transforms/errors etc here.
            balance_tutorial.error.NotEnoughMoneyError,
            balance_tutorial.error.InvalidAmountError,
            balance_tutorial.model.BalanceModel,
            balance_tutorial.transform.CreateUser,
        ]

        for component in components:
          registry.register(component)

```

#### STEP 3: Writing the client code in `new_user.py`

Now that the server code is ready to go, we need to write the client functions in `new_user.py`:

```
from plug.key import ED25519SigningKey
from plug.hash import sha256
from plug.proof import SingleKeyProof
from balance_tutorial.transform import CreateUser
from plug.transaction import Transaction
from plug.constant import TransactionEvent
from plug.message import Event
from plug.registry import Registry
from balance_tutorial.user import User
import aiohttp
import json
import asyncio

async def init_create_user():
    registry = Registry().with_default()
    registry.register(Event)
    registry.register(CreateUser)

    user_obj = {"key" : ED25519SigningKey.to_string(ED25519SigningKey.new()), "nonce" : 0}
    user = User(ED25519SigningKey.from_string(user_obj["key"]))

    user_data = json.load(open("user_data.json", "r"))
    user_data["users"].append(user_obj)

    with open("user_data.json", "w") as write_file:
        json.dump(user_data, write_file)

    transform = CreateUser(
        user=user.address,
    )

    challenge = transform.hash(sha256)
    proof = SingleKeyProof(user.address, user_obj["nonce"], challenge, 'balance_tutorial')
    proof.sign(user.signing_key)
    transaction = Transaction(transform, {proof.address: proof})

    event = Event(
        event=TransactionEvent.ADD,
        payload=transaction
    )

    payload = registry.pack(event)

    async with aiohttp.ClientSession() as session:
        async with session.post("http://localhost:8181/_api/v1/transaction", json=payload) as response:
            data = await response.json()

    print(data)

```

A new signing key is created for our user using the plug's `ED25519SigningKey` class, and we're saving it into the `user_data.json` file. Once we have a record of these signing keys, we can use them to play around with our future Transforms.

To check whether this code is working, we can run the client side code from our terminal. Navigate into the `/client` directory and run `python client.py create_user`. You should see the `NEW USER CREATED` text in your server terminal, and a new entry added to the `user_data.json` file.

#### STEP 4: Create a BalanceQuery class that extends Transform in `transform.py`

Now we're going to write another Transform that can check the balance of a specific User in the blockchain. This code also goes in `transform.py` below the CreateUser class definition:

```
...

@dataclass
class BalanceQuery(Transform):
    fqdn = "tutorial.BalanceQuery"
    user: str

    def required_authorizations(self):
        return {self.user}

    @staticmethod
    def required_models():
        return {BalanceModel.fqdn}

    def required_keys(self):
        return {self.user}

    @staticmethod
    def pack(registry, obj):
        return {
            "user": obj.user,
        }

    @classmethod
    def unpack(cls, registry, payload):
        return cls(
            user=payload["user"],
        )

    def verify(self, state_slice):
        balance = state_slice[BalanceModel.fqdn]

    def apply(self, state_slice):
        balances = state_slice[BalanceModel.fqdn]
        print('-----------')
        print('USER BALANCE: ')
        print(balances[self.user].balance)
        print('-----------')

```

Now that you have created another Transform, you can't forget to add it to the components list in `__init__.py` like you did in STEP 2.

#### STEP 5: Writing the client code for `balance_query.py`

It's time to write the client side code that executes the BalanceQuery Transform in `balance_query.py`:

```
from plug.key import ED25519SigningKey
from plug.hash import sha256
from plug.proof import SingleKeyProof
from balance_tutorial.transform import BalanceQuery
from plug.transaction import Transaction
from plug.constant import TransactionEvent
from plug.message import Event
from plug.registry import Registry
from balance_tutorial.user import User
import aiohttp
import json
import asyncio

async def init_balance_query(signing_key_input):
    registry = Registry().with_default()
    registry.register(Event)
    registry.register(BalanceQuery)

    user_data = json.load(open("user_data.json", "r"))
    user_obj = None

    for i, user in enumerate(user_data["users"]):
        if user_data["users"][i]["key"] == signing_key_input:
            user_data["users"][i]["nonce"] += 1;
            user_obj = user_data["users"][i]
            with open("user_data.json", "w") as write_file:
                json.dump(user_data, write_file)

    if user_obj == None:
        print("no user found with that key")
        return

    user = User(ED25519SigningKey.from_string(signing_key_input))

    transform = BalanceQuery(
        user=user.address,
    )

    challenge = transform.hash(sha256)
    proof = SingleKeyProof(user.address, user_obj["nonce"], challenge, 'balance_tutorial')
    proof.sign(user.signing_key)
    transaction = Transaction(transform, {proof.address: proof})

    event = Event(
        event=TransactionEvent.ADD,
        payload=transaction
    )

    payload = registry.pack(event)

    async with aiohttp.ClientSession() as session:
        async with session.post("http://localhost:8181/_api/v1/transaction", json=payload) as response:
            data = await response.json()

    print(data)

```

This code is very similar to the CreateUser function, but instead of writing a new User to the `user_data.json` file, it reads back from the User array to establish whether the `signing_key` you have entered is valid.

To check this function, we once again run the client side code from our terminal. Navigate into the `/client` directory and run `python client.py balance_query`. You will be prompted to enter the `signing_key` for a User. Copy and paste one of the "key" fields over from `user_data.json`.

All going well, the balance for your queried User should now display over in your server terminal.

#### STEP 6: Write a new FreeMoney Transform over in `transform.py`

Now we're going to write another Transform that gives free money to a specific User. This class requires an `amount` property, and then in the `apply()` method we get a reference to the correct User and add the amount to their balance.

```
@dataclass
class FreeMoney(Transform):
    fqdn = "tutorial.FreeMoney"
    receiver: str
    amount: int

    def required_authorizations(self):
        return {self.receiver}

    @staticmethod
    def required_models():
        return {BalanceModel.fqdn}

    def required_keys(self):
        return {self.receiver}

    @staticmethod
    def pack(registry, obj):
        return {
            "receiver": obj.receiver,
            "amount": obj.amount,
        }

    @classmethod
    def unpack(cls, registry, payload):
        return cls(
            receiver=payload["receiver"],
            amount=payload["amount"],
        )

    def verify(self, state_slice):
        balances = state_slice[BalanceModel.fqdn]

        if self.amount <= 0:
            raise balance_tutorial.error.InvalidAmountError("Transfer amount must be more than 0")

    def apply(self, state_slice):
        balances = state_slice[BalanceModel.fqdn]
        balances[self.receiver].balance += self.amount
```

Don't forget to add the new FreeMoney component over in `__init__.py`!

#### STEP 7: Write the client side code in `free_money.py`

Just like we did for the previous two features, you now need to write the client code that will execute the new Transform code. This happens in `free_money.py`:

```
from plug.key import ED25519SigningKey
from plug.hash import sha256
from plug.proof import SingleKeyProof
from balance_tutorial.transform import FreeMoney
from plug.transaction import Transaction
from plug.constant import TransactionEvent
from plug.message import Event
from plug.registry import Registry
from balance_tutorial.user import User
import aiohttp
import json
import asyncio

async def init_free_money(signing_key_input):
    registry = Registry().with_default()
    registry.register(Event)
    registry.register(FreeMoney)

    user_data = json.load(open("user_data.json", "r"))
    user_obj = None

    for i, user in enumerate(user_data["users"]):
        if user_data["users"][i]["key"] == signing_key_input:
            user_data["users"][i]["nonce"] += 1;
            user_obj = user_data["users"][i]
            with open("user_data.json", "w") as write_file:
                json.dump(user_data, write_file)

    if user_obj == None:
        print("no user found with that key")
        return

    user = User(ED25519SigningKey.from_string(signing_key_input))

    transform = FreeMoney(
        receiver=user.address,
        amount=1000,
    )

    challenge = transform.hash(sha256)
    proof = SingleKeyProof(user.address, user_obj["nonce"], challenge, 'balance_tutorial')
    proof.sign(user.signing_key)
    transaction = Transaction(transform, {proof.address: proof})

    event = Event(
        event=TransactionEvent.ADD,
        payload=transaction
    )

    payload = registry.pack(event)

    async with aiohttp.ClientSession() as session:
        async with session.post("http://localhost:8181/_api/v1/transaction", json=payload) as response:
            data = await response.json()

    print(data)

```

This is also very similar to the previous client function you wrote. But now it passes along an `amount` integer into the FreeMoney Transform.

Try running this code with `python client.py free_money` and enter one of the signing keys from your `user_data.py` file. You should get a success message in your terminal. To confirm the User _did indeed_ receive their free money, try runnning your `python client.py balance_query` command again, and enter the same signing key and check the server terminal log.

#### STEP 8: Create a BalanceTransfer class in `transform.py`

The final feature we're going to implement is the ability to transfer money between two different Users in the blockchain. Once again this is going to happen in `transform.py`:

```
@dataclass
class BalanceTransfer(Transform):
    fqdn = "tutorial.BalanceTransfer"
    sender: str
    receiver: str
    amount: int

    def required_authorizations(self):
        return {self.sender}

    @staticmethod
    def required_models():
        return {BalanceModel.fqdn}

    def required_keys(self):
        return {self.sender, self.receiver}

    @staticmethod
    def pack(registry, obj):
        return {
            "sender": obj.sender,
            "receiver": obj.receiver,
            "amount": obj.amount,
        }

    @classmethod
    def unpack(cls, registry, payload):
        return cls(
            sender=payload["sender"],
            receiver=payload["receiver"],
            amount=payload["amount"],
        )

    def verify(self, state_slice):
        balances = state_slice[BalanceModel.fqdn]

        if self.amount <= 0:
            raise balance_tutorial.error.InvalidAmountError("Transfer amount must be more than 0")

        if balances[self.sender].balance < self.amount:
            raise balance_tutorial.error.NotEnoughMoneyError("Insufficient funds")

    def apply(self, state_slice):
        balances = state_slice[BalanceModel.fqdn]
        balances[self.sender].balance -= self.amount
        balances[self.receiver].balance += self.amount
```

This is the most complicated Transform we have defined so far. It is similar to the FreeMoney class, but must also include information about the sender. All of the action here is going to happen in the `verify()` and `apply()`
