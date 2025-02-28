// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract Governance {
    struct Proposal {
        uint256 id;
        string description;
        uint256 voteCount;
        bool exists;
    }

    mapping(uint256 => Proposal) public proposals;
    mapping(address => mapping(uint256 => bool)) public hasVoted; // Track if an address has voted on a proposal
    uint256 public proposalCount;

    event ProposalCreated(uint256 indexed proposalId, string description);
    event Voted(address indexed voter, uint256 indexed proposalId);

    // Function to create a new proposal
    function createProposal(string memory description) public {
        proposalCount++;
        proposals[proposalCount] = Proposal(proposalCount, description, 0, true);
        emit ProposalCreated(proposalCount, description);
    }

    // Function to vote on a proposal
    function vote(uint256 proposalId) public {
        require(proposals[proposalId].exists, "Proposal does not exist");
        require(!hasVoted[msg.sender][proposalId], "You have already voted on this proposal");

        hasVoted[msg.sender][proposalId] = true; // Mark that the user has voted
        proposals[proposalId].voteCount += 1; // Increment the vote count

        emit Voted(msg.sender, proposalId);
    }

    // Function to get the vote count for a proposal
    function getVoteCount(uint256 proposalId) public view returns (uint256) {
        require(proposals[proposalId].exists, "Proposal does not exist");
        return proposals[proposalId].voteCount;
    }
}
