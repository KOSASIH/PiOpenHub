# piNFTMarketplace/utils.py

import requests

def get_nft_metadata(token_uri):
    """Fetch metadata for an NFT from the given token URI."""
    try:
        response = requests.get(token_uri)
        response.raise_for_status()  # Raise an error for bad responses (4xx and 5xx)
        return response.json()  # Return the JSON response containing metadata
    except requests.exceptions.RequestException as e:
        print(f"Error fetching metadata from {token_uri}: {e}")
        return None

def format_price(price_in_wei):
    """Convert price from Wei to Ether and format it."""
    from web3 import Web3
    price_in_ether = Web3.fromWei(price_in_wei, 'ether')
    return f"{price_in_ether:.4f} ETH"  # Format to 4 decimal places

def validate_token_uri(token_uri):
    """Validate the format of the token URI."""
    if not isinstance(token_uri, str) or not token_uri.startswith("http"):
        raise ValueError("Invalid token URI. It should be a valid URL starting with 'http'.")

# Example usage
if __name__ == "__main__":
    # Example token URI
    example_token_uri = "https://example.com/metadata/1"
    
    # Fetch NFT metadata
    metadata = get_nft_metadata(example_token_uri)
    print(f"NFT Metadata: {metadata}")

    # Format price example
    price_in_wei = 1000000000000000000  # 1 Ether in Wei
    formatted_price = format_price(price_in_wei)
    print(f"Formatted Price: {formatted_price}")

    # Validate token URI
    try:
        validate_token_uri(example_token_uri)
        print("Token URI is valid.")
    except ValueError as e:
        print(f"Token URI validation error: {e}")
