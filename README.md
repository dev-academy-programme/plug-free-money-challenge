Balance Tutorial
==============================

## INTRODUCTION TO PLUG AND TRANSFORMS

### OBJECTIVES
- Create a Transform that adds free money to a specific Users balance.
- Create a Transform that can transfer money between two Users

#### OBJECTIVE: CREATE A FREE MONEY TRANSFORM

##### Step One: Generating a User.

Before we can start handing out any free money we'll need someone to give it to. Navigate into the client repository and run `python client.py create_user`. This should add a new User into the blockchain, and print out their pertinent information in your console.

Make sure to keep a copy of that `signing_key`. We'll use it in all of the future transforms to interact with the User.

##### Step Two: Checking their balance.

All users are created equal in this blockchain. When a new User is added, they receive a starting balance of 100. Try running `python client.py balance_query` from your terminal and enter the `signing_key` from earlier when prompted. This should print the User balance in your log.

##### Step Three: Writing the FreeMoney transform.

Now it's time to write the FreeMoney class in `transform.py`. This class extends Transform, and has several required methods to work correctly. Check out the plug documentation for a reference on writing Transforms.

```
@dataclass
class FreeMoney(Transform):
    fqdn = "tutorial.FreeMoney"
    receiver: str
    amount: int

    def required_authorizations(self):

    @staticmethod
    def required_models():

    def required_keys(self):

    @staticmethod
    def pack(registry, obj):

    @classmethod
    def unpack(cls, registry, payload):

    def verify(self, state_slice):

    def apply(self, state_slice):

```

This is actually a very simple transform. Essentially there are only two things you need to check for. In the `verify(self, state_slice)` method, you need to _verify_ that the amount you are trying to add to the User's balance is _greater than 0._

Then, most important of all, in the `apply(self, state_slice)` method, the actual transformation needs to take place. This will require referencing a `balances` object from the `state_slice[]`, and using your `BalanceModel.fqdn` as the indexer.

Once you have that `balances[]` reference, you can use the address of the the `self.receiver` as an index and increment their balance by the desired amount.

##### Step Four: Add the FreeMoney transform to your components array.

Over in `__init.py__` there is an array of components to include in this Plugin. Make sure you _add your new FreeMoney transform to this list_: `balance_tutorial.transform.FreeMoney,`

```
  components = [
      # Include your plugin's models/transforms/errors etc here.
      balance_tutorial.error.NotEnoughMoneyError,
      balance_tutorial.error.InvalidAmountError,
      balance_tutorial.model.BalanceModel,
  ]
```

##### Step Five: Writing the FreeMoney client.

Head over to `free_money.py`. The first step here is going to be getting a reference to your desired user object. Luckily, because this script is going to be triggered by user input on the command line, we have a `signing_key_input` argument to retrieve the correct user object. This is going to require using the `User.load()` function. If you haven't already, go read `user.py` and make sure you understand exactly what going on there.

Once you have a reference to the correct user, it's time to apply the FreeMoney transform you wrote in `transform.py`. Don't forget to pass in the `receiver` and `amount` arguments.





```
async def init_free_money(signing_key_input):
    registry = Registry().with_default()
    registry.register(Event)
    registry.register(FreeMoney)

    user = await User.load(signing_key_input)

    transform = FreeMoney(
        receiver=user.address,
        amount=1000,
    )

    challenge = transform.hash(sha256)
    proof = SingleKeyProof(user.address, user.nonce, challenge, 'balance.tutorial')
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
