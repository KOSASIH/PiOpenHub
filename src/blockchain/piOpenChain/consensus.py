import hashlib
import time

class Consensus:
    def __init__(self, blockchain):
        self.blockchain = blockchain

    def mine_block(self, miner_address, data):
        """Mine a new block and add it to the blockchain."""
        last_block = self.blockchain.get_last_block()
        previous_hash = last_block.hash if last_block else '0'
        index = len(self.blockchain.chain) + 1
        timestamp = self.get_current_timestamp()

        # Start mining process
        nonce = 0
        difficulty = self.get_difficulty()  # Define the difficulty level
        new_block_hash = self.calculate_hash(index, previous_hash, timestamp, data, nonce)

        while not self.is_valid_proof(new_block_hash, difficulty):
            nonce += 1
            new_block_hash = self.calculate_hash(index, previous_hash, timestamp, data, nonce)

        # Create the new block
        new_block = self.blockchain.create_block(data, previous_hash)
        new_block.nonce = nonce  # Store the nonce in the block
        new_block.hash = new_block_hash  # Update the block's hash

        print(f"Block mined: {new_block}")
        return new_block

    def calculate_hash(self, index, previous_hash, timestamp, data, nonce):
        """Calculate the hash of a block."""
        block_string = f"{index}{previous_hash}{timestamp}{data}{nonce}".encode()
        return hashlib.sha256(block_string).hexdigest()

    def is_valid_proof(self, hash, difficulty):
        """Check if the hash meets the difficulty criteria."""
        return hash[:difficulty] == '0' * difficulty

    def get_current_timestamp(self):
        """Return the current timestamp."""
        return int(time.time())

    def get_difficulty(self):
        """Define the difficulty level for mining."""
        # For simplicity, we can set a static difficulty level
        return 4  # Number of leading zeros required in the hash

# Example usage
if __name__ == "__main__":
    from blockchain import Blockchain  # Import the Blockchain class

    blockchain = Blockchain()
    consensus = Consensus(blockchain)

    # Simulate mining a block
    miner_address = "Miner1"
    data = "Transaction data for the new block"
    consensus.mine_block(miner_address, data)

    # Print the blockchain
    for block in blockchain.chain:
        print(block)
