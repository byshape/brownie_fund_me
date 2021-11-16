import pytest
from brownie import accounts, exceptions, FundMe

from scripts.deploy import deploy_contract
from scripts.fund_and_withdraw import fund, withdraw
# from scripts.helpful_scripts import get_account, get_price_feed


def test_deploy():
    fund_me = deploy_contract()
    assert fund_me.balance() == 0


def test_fund():
    # account = get_account()
    fund_me = deploy_contract()
    fund()
    entrance_fee = fund_me.getEntranceFee() + 100
    assert fund_me.balance() == entrance_fee
    assert fund_me.addressToAmountFunded(fund_me.owner()) == entrance_fee


def test_owner_withdraw():
    fund_me = deploy_contract()
    fund()
    withdraw()
    assert fund_me.balance() == 0
    assert fund_me.addressToAmountFunded(fund_me.owner()) == 0


def test_unauthorized_withdraw():
    account = accounts[1]
    fund_me = deploy_contract()
    fund()
    with pytest.raises(exceptions.VirtualMachineError):
        withdraw(account)
    entrance_fee = fund_me.getEntranceFee() + 100
    assert fund_me.balance() == entrance_fee
    assert fund_me.addressToAmountFunded(fund_me.owner()) == entrance_fee


