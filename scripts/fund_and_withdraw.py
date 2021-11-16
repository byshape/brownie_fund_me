from brownie import FundMe

from scripts.helpful_scripts import get_account


def fund(account=None):
    if not account:
        account = get_account()
    fund_me = FundMe[-1]
    entrance_fee = fund_me.getEntranceFee() + 100
    print(f"The current entry fee is {entrance_fee}")
    transaction = fund_me.fund({"from": account, "value": entrance_fee})


def withdraw(account=None, fund_me=None):
    if not account:
        account = get_account()
    if not fund_me:
        fund_me = FundMe[-1]
    transaction = fund_me.withdraw({"from": account})


def main():
    fund()
    withdraw()
