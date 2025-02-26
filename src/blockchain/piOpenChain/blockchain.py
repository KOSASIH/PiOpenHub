import hashlib
import time
import json

class Block:
    def __init__(self, index, previous_hash, timestamp, data, hash):
        self.index = index
        self.previous_hash = previous_hash
        self.timestamp = timestamp
        self.data = data
        self.hash = hash

    def __repr__(self):
        return json.dumps(self.__dict__, indent=4)

class Blockchain:
    def __init__(self):
        self.chain = []
        self.create_block(previous_hash='0')  # Create the genesis block

    def create_block(self, data, previous_hash):
        """Create a new block and add it to the chain."""
        index = len(self.chain) + 1
        timestamp = self.get_current_timestamp()
        hash = self.calculate_hash(index, previous_hash, timestamp, data)
        block = Block(index, previous_hash, timestamp, data, hash)
        self.chain.append(block)
        return block

    def calculate_hash(self, index, previous_hash, timestamp, data):
        """Calculate the hash of a block."""
        block_string = f"{index}{previous_hash}{timestamp}{data}".encode()
        return hashlib.sha256(block_string).hexdigest()

    def get_current_timestamp(self):
        """Return the current timestamp."""
        return int(time.time())

    def get_last_block(self):
        """Return the last block in the chain."""
        return self.chain[-1] if self.chain else None

    def is_chain_valid(self):
        """Check if the blockchain is valid."""
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]

            # Check if the hash of the current block is correct
            if current_block.previous_hash != previous_block.hash:
                return False

            # Check if the hash is valid
            if current_block.hash != self.calculate_hash(current_block.index, current_block.previous_hash, current_block.timestamp, current_block.data):
                return False

        return True

# Example usage
if __name__ == "__main__":
    blockchain = Blockchain()
    
    # Adding blocks to the blockchain
    blockchain.create_block(data="First block data", previous_hash=blockchain.get_last_block().hash)
    blockchain.create_block(data="Second block data", previous_hash=blockchain.get_last_block().hash)

    # Print the blockchain
    for block in blockchain.chain:
        print(block)

    # Validate the blockchain
    print("Is blockchain valid?", blockchain.is_chain_valid())
