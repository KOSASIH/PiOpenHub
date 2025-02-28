from flask import Flask, request, jsonify
from web3 import Web3

app = Flask(__name__)

# Connect to Ethereum network
w3 = Web3(Web3.HTTPProvider('https://your.ethereum.node'))

# Smart contract ABI and address
contract_address = '0xYourContractAddress'
contract_abi = [...]  # Replace with your contract's ABI

# Initialize contract
contract = w3.eth.contract(address=contract_address, abi=contract_abi)

@app.route('/create_proposal', methods=['POST'])
def create_proposal():
    data = request.json
    title = data.get('title')
    description = data.get('description')
    # Assume the sender is the user making the proposal
    sender = w3.eth.defaultAccount

    # Create a proposal in the smart contract
    tx_hash = contract.functions.createProposal(title, description).transact({'from': sender})
    w3.eth.waitForTransactionReceipt(tx_hash)

    return jsonify({'status': 'Proposal created', 'tx_hash': tx_hash.hex()})


@app.route('/vote', methods=['POST'])
def vote():
    data = request.json
    proposal_id = data.get('proposal_id')
    vote_type = data.get('vote_type')  # 'yes' or 'no'
    sender = w3.eth.defaultAccount

    # Cast a vote in the smart contract
    tx_hash = contract.functions.vote(proposal_id, vote_type).transact({'from': sender})
    w3.eth.waitForTransactionReceipt(tx_hash)

    return jsonify({'status': 'Vote cast', 'tx_hash': tx_hash.hex()})


@app.route('/get_proposals', methods=['GET'])
def get_proposals():
    proposals = contract.functions.getProposals().call()
    return jsonify(proposals)


@app.route('/get_results', methods=['GET'])
def get_results():
    proposal_id = request.args.get('proposal_id')
    results = contract.functions.getProposalResults(proposal_id).call()
    return jsonify({'proposal_id': proposal_id, 'results': results})


if __name__ == '__main__':
    app.run(debug=True)
