from dataclasses import dataclass
from plug.abstract import Transform

from free_money.model import BalanceModel

import free_money.error
import free_money.model

@dataclass
class BalanceTransfer(Transform):
    fqdn = "tutorial.BalanceTransfer"
    sender: str
    receiver: str
    amount: int

    def required_authorizations(self):
        print("place_holder!")

    @staticmethod
    def required_models():
        print("place_holder!")

    def required_keys(self):
        print("place_holder!")

    @staticmethod
    def pack(registry, obj):
        print("place_holder!")

    @classmethod
    def unpack(cls, registry, payload):
        print("place_holder!")

    def verify(self, state_slice):
        print("place_holder!")

    def apply(self, state_slice):
        print("place_holder!")

@dataclass
class FreeMoney(Transform):
    print("Welcome to the Free Money challenge!")
