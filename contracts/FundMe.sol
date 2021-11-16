// SPDX-License-Identifier: GPL-3.0

pragma solidity >=0.7.0 <0.9.0;

import "@chainlink/contracts/src/v0.8/interfaces/AggregatorV3Interface.sol";

contract FundMe {

    address public owner;
    mapping(address => uint256) public addressToAmountFunded;
    address[] public funders;
    AggregatorV3Interface public priceFeed;

    constructor(address _priceFeed) {
        priceFeed = AggregatorV3Interface(_priceFeed);
        owner = msg.sender;
    }

    modifier onlyOwner {
        require(msg.sender == owner, "Only owner is eligible to do it");
        _;
    }

    function fund() public payable {
//        uint256 minimumUSD = 50 * 10 ** 18;
        uint256 minimumUSD = 50 * 10 ** 18;
//        require(getConversionRate(msg.value) >= minimumUSD, "You need more ETH");
        require(msg.value >= getEntranceFee(), "You need more ETH");
        addressToAmountFunded[msg.sender] += msg.value;
        funders.push(msg.sender);
    }

    function withdraw() public payable onlyOwner{
        payable(msg.sender).transfer(address(this).balance);
        for (uint256 funderIndex=0; funderIndex<funders.length; funderIndex++) {
            addressToAmountFunded[funders[funderIndex]] = 0;
        }
        funders = new address[](0);
    }

    function getVersion() public view returns(uint256) {
        return priceFeed.version();
    }

    function getPrice() public view returns(uint256) {
        (,int256 answer,,,) = priceFeed.latestRoundData();
        return uint256(answer * 10000000000);
    }

    function getConversionRate(uint256 ethAmount) public view returns(uint256) {
        return ((ethAmount * getPrice())/(10 ** 18));
    }

    function getEntranceFee() public view returns (uint256) {
        // minimumUSD
        uint256 minimumUSD = 50 * 10 ** 18;
        uint256 price = getPrice();
        uint256 precision = 1 * 10 ** 18;
        return (minimumUSD * precision) / price;
    }
}