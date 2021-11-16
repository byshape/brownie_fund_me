from brownie import config, FundMe

from scripts.helpful_scripts import get_account, get_price_feed, get_publish_source


def deploy_contract():
    account = get_account()
    print(f"Account: {account}")
    # get the priceFeed address
    price_feed_address = get_price_feed()
    print(f"Price feed address: {price_feed_address}")
    # get bool from config: should we verify source code
    publish_source = get_publish_source()
    print(f"Verify: {publish_source}")
    # sending priceFeed contract address to FundMe constructor
    fund_me = FundMe.deploy(price_feed_address,
                            {"from": account}, publish_source=publish_source)

    print(f"Contract deployed to {fund_me}")
    return fund_me


def main():
    deploy_contract()
