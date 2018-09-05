from dataclasses import dataclass
from plug.abstract import Transform

import balance_tutorial.error
import balance_tutorial.model

# Define your plugin's transforms here.

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
        return {balance_tutorial.model.BalanceModel.fqdn}

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
        balances = state[balance_tutorial.model.BalanceModel.fqdn]
        balances[self.sender].balance -= self.amount
        balances[self.receiver].balance += self.amount
