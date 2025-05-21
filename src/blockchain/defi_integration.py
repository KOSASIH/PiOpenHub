# src/blockchain/defi_integration.py

from web3 import Web3
import json
import logging
import requests
from typing import Dict, List, Any, Optional, Union

class DeFiIntegration:
    """
    Integration with DeFi protocols for advanced blockchain functionality.
    
    This class provides methods to interact with various DeFi protocols,
    including decentralized exchanges, lending platforms, and yield farming.
    """
    
    def __init__(self, provider_url: str, chain_id: int = 1):
        """
        Initialize the DeFi integration.
        
        Args:
            provider_url (str): URL of the Ethereum provider (e.g., Infura, Alchemy)
            chain_id (int): Chain ID (1 for Ethereum mainnet, 137 for Polygon, etc.)
        """
        self.web3 = Web3(Web3.HTTPProvider(provider_url))
        self.chain_id = chain_id
        self.logger = logging.getLogger(__name__)
        
        # Common DeFi protocol addresses (example addresses - would be updated in production)
        self.protocol_addresses = {
            'uniswap_v3_router': '0xE592427A0AEce92De3Edee1F18E0157C05861564',
            'aave_v3_pool': '0x87870Bca3F3fD6335C3F4ce8392D69350B4fA4E2',
            'compound_v3': '0xc3d688B66703497DAA19211EEdff47f25384cdc3',
            'curve_pool_registry': '0x90E00ACe148ca3b23Ac1bC8C240C2a7Dd9c2d7f5'
        }
        
    def is_connected(self) -> bool:
        """Check if connected to the blockchain."""
        return self.web3.is_connected()
        
    def get_token_balance(self, token_address: str, wallet_address: str) -> float:
        """
        Get the balance of a specific token for a wallet.
        
        Args:
            token_address (str): Address of the ERC20 token
            wallet_address (str): Address of the wallet
            
        Returns:
            float: Token balance in human-readable format
        """
        # ERC20 ABI for balanceOf function
        abi = [
            {
                "constant": True,
                "inputs": [{"name": "_owner", "type": "address"}],
                "name": "balanceOf",
                "outputs": [{"name": "balance", "type": "uint256"}],
                "type": "function"
            },
            {
                "constant": True,
                "inputs": [],
                "name": "decimals",
                "outputs": [{"name": "", "type": "uint8"}],
                "type": "function"
            }
        ]
        
        try:
            # Create contract instance
            token_contract = self.web3.eth.contract(address=token_address, abi=abi)
            
            # Get token decimals
            decimals = token_contract.functions.decimals().call()
            
            # Get raw balance
            raw_balance = token_contract.functions.balanceOf(wallet_address).call()
            
            # Convert to human-readable format
            balance = raw_balance / (10 ** decimals)
            
            return balance
        except Exception as e:
            self.logger.error(f"Error getting token balance: {e}")
            return 0.0
            
    def get_token_price(self, token_address: str, vs_currency: str = 'usd') -> float:
        """
        Get the current price of a token using CoinGecko API.
        
        Args:
            token_address (str): Address of the token
            vs_currency (str): Currency to get price in (e.g., 'usd', 'eth')
            
        Returns:
            float: Current token price
        """
        try:
            # Get token price from CoinGecko
            url = f"https://api.coingecko.com/api/v3/simple/token_price/ethereum?contract_addresses={token_address}&vs_currencies={vs_currency}"
            response = requests.get(url)
            data = response.json()
            
            # Extract price
            price = data.get(token_address.lower(), {}).get(vs_currency, 0.0)
            
            return float(price)
        except Exception as e:
            self.logger.error(f"Error getting token price: {e}")
            return 0.0
            
    def swap_tokens(
        self, 
        token_in: str, 
        token_out: str, 
        amount_in: int,
        min_amount_out: int,
        wallet_address: str,
        private_key: str,
        deadline: Optional[int] = None,
        slippage: float = 0.005  # 0.5% slippage
    ) -> str:
        """
        Swap tokens using Uniswap V3.
        
        Args:
            token_in (str): Address of input token
            token_out (str): Address of output token
            amount_in (int): Amount of input token (in wei)
            min_amount_out (int): Minimum amount of output token (in wei)
            wallet_address (str): Address of the wallet
            private_key (str): Private key for signing transaction
            deadline (int, optional): Transaction deadline timestamp
            slippage (float): Maximum slippage allowed
            
        Returns:
            str: Transaction hash
        """
        # This is a simplified implementation
        # In a real implementation, you would:
        # 1. Get the Uniswap router contract
        # 2. Approve the router to spend your tokens
        # 3. Call the exactInputSingle or exactInput function
        # 4. Sign and send the transaction
        
        self.logger.info(f"Swapping {amount_in} of {token_in} for {token_out}")
        
        # Example implementation (not functional without proper ABI and setup)
        try:
            # Get router contract (simplified)
            router_address = self.protocol_addresses['uniswap_v3_router']
            router_abi = []  # Would need the actual ABI
            
            router = self.web3.eth.contract(address=router_address, abi=router_abi)
            
            # Approve tokens (simplified)
            # token_contract = self.web3.eth.contract(address=token_in, abi=token_abi)
            # approve_tx = token_contract.functions.approve(router_address, amount_in).build_transaction({
            #     'from': wallet_address,
            #     'nonce': self.web3.eth.get_transaction_count(wallet_address),
            #     'gas': 100000,
            #     'gasPrice': self.web3.eth.gas_price
            # })
            # signed_approve_tx = self.web3.eth.account.sign_transaction(approve_tx, private_key)
            # self.web3.eth.send_raw_transaction(signed_approve_tx.rawTransaction)
            
            # Swap tokens (simplified)
            # swap_tx = router.functions.exactInputSingle({
            #     'tokenIn': token_in,
            #     'tokenOut': token_out,
            #     'fee': 3000,  # 0.3% fee tier
            #     'recipient': wallet_address,
            #     'deadline': deadline or (int(time.time()) + 1800),  # 30 minutes from now
            #     'amountIn': amount_in,
            #     'amountOutMinimum': min_amount_out,
            #     'sqrtPriceLimitX96': 0  # No price limit
            # }).build_transaction({
            #     'from': wallet_address,
            #     'nonce': self.web3.eth.get_transaction_count(wallet_address),
            #     'gas': 300000,
            #     'gasPrice': self.web3.eth.gas_price
            # })
            # signed_swap_tx = self.web3.eth.account.sign_transaction(swap_tx, private_key)
            # tx_hash = self.web3.eth.send_raw_transaction(signed_swap_tx.rawTransaction)
            
            # Return transaction hash
            # return tx_hash.hex()
            
            # For demonstration purposes, return a dummy transaction hash
            return "0x0000000000000000000000000000000000000000000000000000000000000000"
        except Exception as e:
            self.logger.error(f"Error swapping tokens: {e}")
            return ""
            
    def get_lending_markets(self) -> List[Dict[str, Any]]:
        """
        Get available lending markets from Aave.
        
        Returns:
            list: List of lending markets with details
        """
        # This would typically involve calling the Aave API or contract
        # For demonstration, return sample data
        return [
            {
                "token": "USDC",
                "address": "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48",
                "supply_apy": 0.0312,  # 3.12%
                "borrow_apy": 0.0412,  # 4.12%
                "total_supply": 1000000000,
                "total_borrow": 800000000
            },
            {
                "token": "ETH",
                "address": "0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE",
                "supply_apy": 0.0212,  # 2.12%
                "borrow_apy": 0.0312,  # 3.12%
                "total_supply": 500000,
                "total_borrow": 300000
            }
        ]
        
    def supply_to_lending_pool(
        self,
        token_address: str,
        amount: int,
        wallet_address: str,
        private_key: str
    ) -> str:
        """
        Supply tokens to a lending pool (e.g., Aave).
        
        Args:
            token_address (str): Address of the token to supply
            amount (int): Amount to supply (in wei)
            wallet_address (str): Address of the wallet
            private_key (str): Private key for signing transaction
            
        Returns:
            str: Transaction hash
        """
        # This is a simplified implementation
        # In a real implementation, you would:
        # 1. Get the Aave pool contract
        # 2. Approve the pool to spend your tokens
        # 3. Call the supply function
        # 4. Sign and send the transaction
        
        self.logger.info(f"Supplying {amount} of {token_address} to lending pool")
        
        # For demonstration purposes, return a dummy transaction hash
        return "0x0000000000000000000000000000000000000000000000000000000000000000"
        
    def get_yield_farming_opportunities(self) -> List[Dict[str, Any]]:
        """
        Get available yield farming opportunities.
        
        Returns:
            list: List of yield farming opportunities with details
        """
        # This would typically involve calling various DeFi protocols
        # For demonstration, return sample data
        return [
            {
                "protocol": "Curve",
                "pool_name": "3pool",
                "tokens": ["DAI", "USDC", "USDT"],
                "apy": 0.0512,  # 5.12%
                "tvl": 1200000000
            },
            {
                "protocol": "Convex",
                "pool_name": "cvxCRV",
                "tokens": ["CRV"],
                "apy": 0.1212,  # 12.12%
                "tvl": 500000000
            }
        ]

# Example usage
if __name__ == "__main__":
    # Initialize DeFi integration with Ethereum mainnet
    defi = DeFiIntegration("https://mainnet.infura.io/v3/your_infura_project_id")
    
    # Check connection
    if defi.is_connected():
        print("Connected to Ethereum network")
        
        # Get token balance
        usdc_address = "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48"  # USDC
        wallet_address = "0xYourWalletAddress"
        balance = defi.get_token_balance(usdc_address, wallet_address)
        print(f"USDC Balance: {balance}")
        
        # Get token price
        price = defi.get_token_price(usdc_address)
        print(f"USDC Price: ${price}")
        
        # Get lending markets
        markets = defi.get_lending_markets()
        print(f"Available lending markets: {markets}")
        
        # Get yield farming opportunities
        opportunities = defi.get_yield_farming_opportunities()
        print(f"Yield farming opportunities: {opportunities}")
    else:
        print("Failed to connect to Ethereum network")