import pytest

from plug.consensus.state import generate_initial_state
from plug.consensus.state import Namespace
from plug.key import ED25519SigningKey
from plug.model import NonceModel
from plug.util import plug_address
from plug.util import prepare_state_slice
from plug.util import sha256

import balance_tutorial.error
import balance_tutorial.model
import balance_tutorial.transform


class User:
    def __init__(self, signing_key, nonce=0):
        self.signing_key = signing_key
        self.nonce = nonce
        self.address = plug_address(signing_key)


@pytest.fixture
def alice():
    return User(ED25519SigningKey.new())


@pytest.fixture
def bob():
    return User(ED25519SigningKey.new())


@pytest.fixture
def state_factory():
    def factory(registry):
        state_dict = {
            # populate default models here
            NonceModel.fqdn: {},
        }

        return generate_initial_state(state_dict, Namespace, registry, sha256)
    return factory


@pytest.fixture
def state_slice_factory():
    def factory(state, transactions, block=None, hashfn=sha256):
        return prepare_state_slice(state, transactions, block=block, hashfn=hashfn)
    return factory
