from plug.abstract import ModelIndexer
from plug.abstract import RunnerIndexer
from plug.indexer import PersistToFileMixin


class BalanceIndexer(PersistToFileMixin, RunnerIndexer):
    fqdn = "tutorial.BalanceIndexer"

    def update(self, state_key, state_slice):
        balances = state_slice['tutorial.BalanceModel']
        self['all'] = {}
        for address in balances:
            self['all'][address] = balances[address].balance

    def remove(self, key, value=None):
        if value is None:
            del self['all'][key]
        else:
            self['all'][key]

