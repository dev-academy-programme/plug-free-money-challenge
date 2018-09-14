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
            raise free_money.error.InvalidAmountError("Transfer amount must be more than 0")

        if balances[self.sender].balance < self.amount:
            raise free_money.error.NotEnoughMoneyError("Insufficient funds")

    def apply(self, state_slice):
        balances = state_slice[BalanceModel.fqdn]
        balances[self.sender].balance -= self.amount
        balances[self.receiver].balance += self.amount

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
            raise free_money.error.InvalidAmountError("Transfer amount must be more than 0")

    def apply(self, state_slice):
        balances = state_slice[BalanceModel.fqdn]
        balances[self.receiver].balance += self.amount