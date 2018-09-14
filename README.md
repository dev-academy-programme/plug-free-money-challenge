Balance Tutorial
==============================

## INTRODUCTION TO PLUG AND TRANSFORMS

### OBJECTIVES
- Create a Transform that adds free money to a specific Users balance.
- Create a Transform that can transfer money between two Users

#### OBJECTIVE: CREATE A FREE MONEY TRANSFORM

First, we're going to create a new FreeMoney class that extends Transform. This transform will allow us to give some free money to a specific user.

##### Step One: Generating a User.

Before we can start handing out any free money, we'll need someone to give it to. Navigate into the client repository and run `python client.py create_user`. This should add a new User into the blockchain, and print out their pertinent information in your console.

Remember to keep a copy of the new User's `address` and `signing_key`. You will need these later! We'll use them to transform and query the blockchain.

##### Step Two: Checking their balance.

All users are created equal in this blockchain. When a new User is added, they receive a starting balance of 100. Try running `python client.py balance_query` from your terminal and enter the `address` from earlier when prompted. This should print the User balance in your log.

##### Step Three: Writing the FreeMoney transform.

Now it's time to write the FreeMoney class in `transform.py`. This class extends Transform, and has several required methods to work correctly. *Check out the plug documentation for a reference on writing Transforms.*

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

You still need to flesh out the other required methods too, but they are fairly standard. Remember to  *Check out the plug documentation for a reference on writing Transforms.*

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

The rest of the client code in `free_money.py` will be fairly boilerplate, and won't differ too much from transform to transform. For more information on challenges, proofs and transactions, please refer to the Plug documentation.

##### Step Six: Give some free money.

Try running `python client.py free_money` from your client directory. After POST-ing the entire affair to the Plug API, you should receive a OK status code back. To double check that our User did indeed receive their free money, run `python client.py balance_query` again with the same `signing_key` and their balance should have increased significantly.

Congratulations! You have successfully written a Transform that gives unlimited, free money to a specific User in the blockchain. Please note; _it is unlikely that your employer will ever request that this specific feature be implemented for financial reasons._

#### OBJECTIVE: CREATE A BALANCE TRANSFER TRANSFORM

Now that we can give users money, we're going to write a new BalanceTransfer class that extends Transform. This transform will be able to transfer money from the balance of one user to another.

##### Step One: Generating another User.

There must be multiple Users within the blockchain to allow the transfer of money back and forth. Run `python client.py create_user` from your client directory again. Remember to keep a copy of the new User's `address` and `signing_key`.

##### Step Two: Writing the BalanceTransfer transform.

Once again it's time to head over to `transform.py`. Define a new `BalanceTransfer` class that extends Transform, and fill in the required methods. If you get stuck, remember to _consult the Plug documentation on writing Transforms_.

Just like in the FreeMoney transform, the real logic takes place in the `verify()` and `apply()` methods. In `verify()`, you need to make sure that the sender actually _has_ a sufficient balance to cover the transfer, and then in `apply()` you will alter the user balances.

##### Step Three: Writing the BalanceTransfer client code:
