from brownie import accounts, config, network, MockV3Aggregator

DECIMALS = 8
STARTING_PRICE = 4600 * 10 ** 8
LOCAL_BLOCKCHAIN_ENVIRONMENTS = ["development", "ganache-local"]
FORKED_BLOCKCHAIN_ENVIRONMENTS = ["mainnet-fork", "mainnet-fork-dev"]


def is_local_chain():
    return network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS or \
           network.show_active() in FORKED_BLOCKCHAIN_ENVIRONMENTS


def get_account():
    if is_local_chain():
        return accounts[0]
    else:
        return accounts.add(config["wallets"]["from_key"])


def get_publish_source():
    return config["networks"][network.show_active()].get("verify")


def get_price_feed():
    if is_local_chain():
        if len(MockV3Aggregator) == 0:
            MockV3Aggregator.deploy(DECIMALS, STARTING_PRICE, {"from": get_account()})
        return MockV3Aggregator[-1].address
    else:
        return accounts.add(config["networks"][network.show_active()]["eth_usd_price_feed"])
