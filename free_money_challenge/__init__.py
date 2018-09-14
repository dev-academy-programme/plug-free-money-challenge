from plug.abstract import Plugin

import free_money_challenge.error
import free_money_challenge.model
import free_money_challenge.transform


class FreeMoneyPlugin(Plugin):
    @classmethod
    def setup(cls, registry):
        components = [
            # Include your plugin's models/transforms/errors etc here.
            free_money_challenge.error.NotEnoughMoneyError,
            free_money_challenge.error.InvalidAmountError,
            free_money_challenge.model.BalanceModel,
            free_money_challenge.transform.BalanceTransfer,
            free_money_challenge.transform.FreeMoney,
        ]

        for component in components:
          registry.register(component)
