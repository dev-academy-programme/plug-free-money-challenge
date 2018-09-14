from dataclasses import dataclass

from plug.abstract import Model

# Define your plugin's models here.

@dataclass
class BalanceModel(Model):
    fqdn = "tutorial.BalanceModel"
    balance: int = 0

    @classmethod
    def default_factory(cls):
        return cls(balance = 100)

    @staticmethod
    def pack(registry, obj):
        return {
            "balance": obj.balance,
        }

    @classmethod
    def unpack(cls, registry, payload):
        return cls(
            balance=payload["balance"]
        )
