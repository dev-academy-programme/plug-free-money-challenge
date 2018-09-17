import pytest
from pathlib import Path

# from plug.consensus.state import generate_initial_state
# from plug.consensus.state import Namespace
from plug.key import ED25519SigningKey
from plug.model import NonceModel
from plug.util import plug_address
from plug.util import prepare_state_slice
from plug.hash import sha256

from plug.cli.schema import DEVELOP_NETWORK
from plug.cli.util import init_registry
from plug.config import Config
from plug_api.key_managers.memory import InMemoryKeyManager


import free_money.error
import free_money.model
import free_money.transform

import free_money
#
#
@pytest.fixture(name="dapp_registry")
def fixture_dapp_registry():
    """
    Returns a registry object pre-configured with the ÐApp's models and
    transforms.
    """
    # Load ÐApp models and transforms from the node configuration.
    config_file = (Path(free_money.__path__[0]) / ".." / "config.yaml").resolve()
    config = Config(DEVELOP_NETWORK).load(config_file)
    return init_registry(config)

@pytest.fixture(name="key_manager")
def fixture_key_manager():
    """
    Returns a key manager for use in unit tests.
    """
    return InMemoryKeyManager()
