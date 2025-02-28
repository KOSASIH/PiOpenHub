// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract ShardedStorage {
    // Mapping to store balances for each shard
    mapping(uint256 => mapping(address => uint256)) public shardBalances;

    // Event declarations
    event Deposit(uint256 indexed shardId, address indexed user, uint256 amount);
    event Withdraw(uint256 indexed shardId, address indexed user, uint256 amount);

    // Deposit function to add funds to a specific shard
    function deposit(uint256 shardId) public payable {
        require(msg.value > 0, "Deposit amount must be greater than zero");
        shardBalances[shardId][msg.sender] += msg.value;
        emit Deposit(shardId, msg.sender, msg.value);
    }

    // Withdraw function to remove funds from a specific shard
    function withdraw(uint256 shardId, uint256 amount) public {
        require(shardBalances[shardId][msg.sender] >= amount, "Insufficient balance");
        shardBalances[shardId][msg.sender] -= amount;
        payable(msg.sender).transfer(amount);
        emit Withdraw(shardId, msg.sender, amount);
    }

    // Function to check the balance of a user in a specific shard
    function getShardBalance(uint256 shardId) public view returns (uint256) {
        return shardBalances[shardId][msg.sender];
    }
}
