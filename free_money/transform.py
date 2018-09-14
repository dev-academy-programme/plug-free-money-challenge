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

    @staticmethod
    def required_models():

    def required_keys(self):

    @staticmethod
    def pack(registry, obj):

    @classmethod
    def unpack(cls, registry, payload):

    def verify(self, state_slice):

    def apply(self, state_slice):

@dataclass
class FreeMoney(Transform):
