from plug.abstract import Plugin

import free_money.error
import free_money.model
import free_money.transform


class FreeMoneyPlugin(Plugin):
    @classmethod
    def setup(cls, registry):
        components = [
            # Include your plugin's models/transforms/errors etc here.
            free_money.error.NotEnoughMoneyError,
            free_money.error.InvalidAmountError,
            free_money.model.BalanceModel,
            free_money.transform.BalanceTransfer,
            free_money.transform.FreeMoney,
        ]

        for component in components:
          registry.register(component)
