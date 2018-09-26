import pytest

from free_money.model import BalanceModel

@pytest.mark.skip()
def test_balance_model_initial_balance():
    """ARRANGE"""
    expected_balance = 0

    """ACT"""
    model = BalanceModel()

    """ASSERT"""
    assert model.balance == expected_balance

@pytest.mark.skip()
def test_balance_model_set_balance():
    """ARRANGE"""
    balance = 100
    expected_balance = balance

    """ACT"""
    model = BalanceModel(balance)

    """ASSERT"""
    assert model.balance == expected_balance
