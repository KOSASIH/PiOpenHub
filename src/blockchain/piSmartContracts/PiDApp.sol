// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

interface IPiNetwork {
    function transfer_pi(address recipient, uint256 amount) external returns (bool);
}

contract PiDApp {
    uint256 constant PI_VALUE = 31415900; // In micro units
    address public pi_network;

    event PaymentMade(address indexed payer, address indexed recipient, uint256 amount);
    event PaymentFailed(address indexed payer, address indexed recipient, uint256 amount, string reason);

    constructor(address _pi_network) {
        require(_pi_network != address(0), "Invalid Pi network address");
        pi_network = _pi_network;
    }

    function pay_with_pi(address recipient, uint256 amount) public {
        require(amount > 0, "Amount must be greater than zero");
        uint256 totalAmount = amount * PI_VALUE;

        // Attempt to transfer Pi
        bool success = IPiNetwork(pi_network).transfer_pi(recipient, totalAmount);
        if (success) {
            emit PaymentMade(msg.sender, recipient, totalAmount);
        } else {
            emit PaymentFailed(msg.sender, recipient, totalAmount, "Pi payment failed");
            revert("Pi payment failed");
        }
    }
}
