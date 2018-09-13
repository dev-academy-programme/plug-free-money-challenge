from plug.abstract import Plugin

import balance_tutorial.error
import balance_tutorial.model
import balance_tutorial.transform


class BalanceTutorialPlugin(Plugin):
    @classmethod
    def setup(cls, registry):
        components = [
            # Include your plugin's models/transforms/errors etc here.
            balance_tutorial.error.NotEnoughMoneyError,
            balance_tutorial.error.InvalidAmountError,
            balance_tutorial.model.BalanceModel,
            balance_tutorial.transform.BalanceTransfer,
            balance_tutorial.transform.FreeMoney,
            balance_tutorial.transform.CreateUser,
        ]

        for component in components:
          registry.register(component)
