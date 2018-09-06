Balance Tutorial
==============================

## FREE MONEY CHALLENGE

### OBJECTIVE
Create a Transform that adds money to a specific users balance.

### ROUGH OUTLINE
-  Create a new FreeMoney class in `transform.py` that inherits from `Transform`.
-  Specify which parts of the model will be transformed, and write the required methods.
-  Add the new FreeMoney transform as an included component in the `__init__.py` script for inclusion in the registry.
-  Write client side code that retrieves a User by their `signing_key`.
-  Transform the User model using the FreeMoney class.
-  Record the transformation event into the registry.
-  Post the event up to the API and verify its success.

#### Step 1: Create a FreeMoney class in `transform.py`
The FreeMoney class inherits from Transform, and has several required methods. Use the BalanceTransfer class as a template.

```
@dataclass
class FreeMoney(Transform):
    fqdn = "tutorial.FreeMoney"
    ...

    def required_authorizations(self):
        ...

    @staticmethod
    def required_models():
        ...

    def required_keys(self):
        ...

    @staticmethod
    def pack(registry, obj):
        ...

    @classmethod
    def unpack(cls, registry, payload):
        ...

    def verify(self, state_slice):
        ...

    def apply(self, state_slice):
        ...

```

#### Step 2: Writing the client code in `freemoney.py`

```
from balance_tutorial.transform import FreeMoney

...

async def main():
    # registering the free money event
    # loading the user data
    # transforming the data
    # challenges and proofs
    # creating and registering the transform event
    # async posting it to the API

...

```

#### STEP 3: BECOME THE BLOCKCHAIN
